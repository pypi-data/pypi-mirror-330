from base_objects import (
    AbstractServerEndpoint,
    AbstractDesktopEndpoint,
    AbstractWindowsEndpoint,
)

from firewheel.control.experiment_graph import AbstractPlugin


class AddWindowsUtilities(AbstractPlugin):
    """Adding various Windows utilities to each Windows VM."""

    def run(self):
        """
        Adding various Windows utilities to each Windows VM.

        This includes adding:
            * ``PuTTY``
            * ``puttygen``
            * ``PSCP``
            * ``Sysmon``
        """
        for v in self.g.get_vertices():
            if not v.is_decorated_by(AbstractWindowsEndpoint):
                continue
            elif v.is_decorated_by(AbstractDesktopEndpoint):
                v.drop_file(-75, "/Users/user/Desktop/putty.exe", "putty.exe")
                v.drop_file(-74, "/Users/user/Desktop/puttygen.exe", "puttygen.exe")
                v.drop_file(-73, "/Users/user/Desktop/pscp.exe", "pscp.exe")
                v.run_executable(
                    -73, "Sysmon64.exe", "-i -n -accepteula", vm_resource=True
                )
            elif v.is_decorated_by(AbstractServerEndpoint):
                v.drop_file(-75, "/Users/Administrator/Desktop/putty.exe", "putty.exe")
                v.drop_file(
                    -74, "/Users/Administrator/Desktop/puttygen.exe", "puttygen.exe"
                )
                v.drop_file(-73, "/Users/Administrator/Desktop/pscp.exe", "pscp.exe")
                v.run_executable(
                    -73, "Sysmon64.exe", "-i -n -accepteula", vm_resource=True
                )
