from windows.windows_7_enterprise import Windows7Enterprise

from firewheel.control.experiment_graph import Vertex, AbstractPlugin


class VmGen(AbstractPlugin):
    """
    This plugin will create as many Windows7Enterprise VMs as the size specifies.
    The new VMs will be give the name server-X where X is an integer.
    """

    def run(self, size="1"):
        """
        This plugin will create as many Windows7Enterprise VMs as the size specifies.

        Args:
            size (str): The number of VMs to create. This must be castable to an :obj:`int`.
        """
        size = int(size)

        for i in range(size):
            vm = Vertex(self.g, "server-%s" % i)
            vm.decorate(Windows7Enterprise)
