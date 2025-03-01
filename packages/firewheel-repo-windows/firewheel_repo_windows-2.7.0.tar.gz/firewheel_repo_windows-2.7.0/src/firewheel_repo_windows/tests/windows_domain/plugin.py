from netaddr import IPNetwork
from base_objects import Switch
from windows.domain_controller import DomainController
from windows.windows_7_enterprise import Windows7Enterprise
from windows.windows_server_2008_r2 import WindowsServer2008R2

from firewheel.control.experiment_graph import Vertex, AbstractPlugin


class WindowsDomain(AbstractPlugin):
    """Creates a topology with a Domain Controller and a given number of Windows hosts."""

    def run(self, size="1"):
        """Create the topology

        Args:
            size(str): The number of windows hosts to create. This must be castable to an :obj:`int`.
        """
        size = int(size)
        network = IPNetwork("192.168.150.0/24")

        switch = Vertex(self.g, "switch.acme.com")
        switch.decorate(Switch)

        dc = Vertex(self.g, "dc.acme.com")

        # Still need to specify the type of domain controller you want
        dc.decorate(WindowsServer2008R2)
        dc.decorate(DomainController, init_args=["acme", "acme.com", "acme"])
        dc.connect(switch, network[1], network.netmask)

        dc.add_user("johndoe", "ChangeThisPassword#2")

        # Create many hosts and have them connect to the domain
        for i in range(size):
            winhost = Vertex(self.g, f"host-{i}.acme.com")
            winhost.decorate(Windows7Enterprise)
            winhost.connect(switch, network[i + 2], network.netmask)
            winhost.join_domain("acme", "acme.com")
