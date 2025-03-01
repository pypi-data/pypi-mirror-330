# UNCLASSIFIED

from netaddr import IPNetwork
from base_objects import Switch
from windows.domain_controller import DomainController
from windows.windows_7_enterprise import Windows7Enterprise
from windows.windows_server_2008_r2 import (
    WindowsServer2008R2,
    WindowsServer2008R2Sysprep,
)

from firewheel.control.experiment_graph import Vertex, AbstractPlugin


class WindowsDomainTrusts(AbstractPlugin):
    """
    Creates a topology with two Domain Controllers with bidirectional trust.
    """

    def run(self):
        """Function to create the topology"""

        network = IPNetwork("192.168.150.0/24")

        switch = Vertex(self.g, "switch.acme.com")
        switch.decorate(Switch)

        dc = Vertex(self.g, "dc.acme.com")
        # Still need to specify the type of domain controller you want
        dc.decorate(WindowsServer2008R2)
        dc.decorate(DomainController, init_args=["acme", "acme.com", "acme"])
        dc.connect(switch, network[1], network.netmask)

        dc.add_user("johndoe", "ChangeThisPassword#2")

        # Add DNS forwarder
        dc.add_conditional_forwarder(-47, "bill.com", str(network[10]))

        winhost = Vertex(self.g, "host.acme.com")
        winhost.decorate(Windows7Enterprise)

        winhost.connect(switch, network[2], network.netmask)
        winhost.join_domain("acme", "acme.com")

        dc2 = Vertex(self.g, "domain.bill.com")
        dc2.decorate(WindowsServer2008R2Sysprep)
        dc2.decorate(DomainController, init_args=["bill", "bill.com", "bill"])
        dc2.connect(switch, network[10], network.netmask)

        dc2.add_user("johndoe", "ChangeThisPassword#2")

        # Add DNS forwarder and set up the trust
        dc2.add_conditional_forwarder(-47, "acme.com", str(network[1]))
        dc2.add_bidirectional_trust(
            -1, "acme.com", "Administrator", "ChangeThisPassword#1"
        )

        winhost = Vertex(self.g, "host.bill.com")
        winhost.decorate(Windows7Enterprise)

        winhost.connect(switch, network[11], network.netmask)
        winhost.join_domain("bill", "bill.com")
