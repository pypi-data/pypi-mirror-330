from windows.base_objects import WindowsHost

from firewheel.control.experiment_graph import AbstractPlugin


class AddFirefox(AbstractPlugin):
    """Add Firefox version 66.0.3 to all Windows VMs."""

    def run(self):
        """Add Firefox version 66.0.3 to all Windows VMs."""
        for v in self.g.get_vertices():
            if v.is_decorated_by(WindowsHost):
                v.run_executable(-75, "FirefoxSetup66-0-3.exe", "/s", vm_resource=True)
