# UNCLASSIFIED

import netaddr
from base_objects import Switch
from generic_vm_objects import GenericRouter
from windows.windows_7_enterprise import Windows7Enterprise

from firewheel.control.experiment_graph import Vertex, AbstractPlugin


class RouterTree(AbstractPlugin):
    """This creates a router high-degree tree running OSPF and BGP.

    Following is an example of a 3 degree tree: ::

      <host> -- <OSPF> -- <BGP 1> -------------------------
                                  |           |           |
                                <B 2>       <B 3>       <B 4>
                                  |           |           |
                                <OSPF>      <OSPF>      <OSPF>
                                  |           |           |
                                <host>      <host>      <host>

    The root has the IP space 10.0.0.0/24.
    """

    def run(self, size, host_image=""):
        """
        Creates the router tree topology.

        Args:
            size (str): The degree of the router tree. This must be castable to an :obj:`int`.
            host_image (str): The name of the image to use for the hosts.
        """
        size = int(size)
        self.host_image = host_image

        control_nets = netaddr.IPNetwork("192.168.0.0/16").subnet(30)
        host_nets = netaddr.IPNetwork("10.0.0.0/8").subnet(24)
        as_nums = iter(range(1, size + 2))

        # First, make the root pair.
        root = self._make_router_pair("root.net", control_nets, host_nets, as_nums)

        # This needs lots of memory if the topology is large
        try:
            root.vm["mem"] = 4096
        except AttributeError:
            root.vm = {"mem": 4096}

        # Next, create all of the leaves and link them to the root.
        for i in range(size):
            leaf = self._make_router_pair(
                "leaf-%d.net" % (i,), control_nets, host_nets, as_nums
            )

            switch = Vertex(self.g)
            switch.decorate(Switch, init_args=["root-leaf%d.switch" % (i,)])

            bgp_net = next(control_nets)
            bgp_ips = bgp_net.iter_hosts()

            leaf.connect(switch, next(bgp_ips), bgp_net.netmask)
            root.connect(switch, next(bgp_ips), bgp_net.netmask)

            root.link_bgp(leaf, switch, switch)

            assert len(root.interfaces.interfaces) != 0
            assert len(leaf.interfaces.interfaces) != 0

    def _make_router_pair(self, name, control_nets, host_nets, as_nums):
        """Internal function to create the host, OSPF, BGP sequence.

        Args:
            name (str): The name of the router/host sequence (e.g. 'leaf-1.net').
            control_nets (netaddr.IPNetwork): The network to use between routers.
            host_nets (netaddr.IPNetwork): The network to use between hosts.
            as_nums (range_iterator): An iterator for the AS numbering of the BGP routers.

        Returns:
            generic_vm_objects.GenericRouter: The BGP router for the pairing.
        """
        host_net = next(host_nets)
        host_ips = host_net.iter_hosts()

        host = Vertex(self.g, "whost.%s" % (name,))
        host.decorate(Windows7Enterprise)

        ospf_net = next(control_nets)
        ospf_ips = ospf_net.iter_hosts()

        ospf = Vertex(self.g, "ospf.%s" % (name,))
        ospf.decorate(GenericRouter)

        as_num = next(as_nums)
        bgp = Vertex(self.g, "bgp.%s" % (name,))
        bgp.decorate(GenericRouter)
        bgp.set_bgp_as(as_num)

        switch_h_o = Vertex(self.g)
        switch_h_o.decorate(Switch, init_args=["switch-host-ospf.%s" % (name,)])

        switch_o_b = Vertex(self.g)
        switch_o_b.decorate(Switch, init_args=["switch-ospf-bgp.%s" % (name,)])

        ospf.connect(switch_h_o, next(host_ips), host_net.netmask)
        host.connect(switch_h_o, next(host_ips), host_net.netmask)

        ospf.ospf_connect(switch_o_b, next(ospf_ips), ospf_net.netmask)
        bgp.ospf_connect(switch_o_b, next(ospf_ips), ospf_net.netmask)

        ospf.redistribute_ospf_connected()
        bgp.redistribute_bgp_into_ospf()
        bgp.redistribute_ospf_into_bgp()

        return bgp
