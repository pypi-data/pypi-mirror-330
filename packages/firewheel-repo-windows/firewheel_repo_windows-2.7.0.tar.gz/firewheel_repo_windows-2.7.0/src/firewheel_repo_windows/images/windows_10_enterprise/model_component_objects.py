from windows.base_objects import WindowsHost

from firewheel.control.experiment_graph import require_class


@require_class(WindowsHost)
class WindowsServer2012R2(object):
    """The Model Component for the Windows 10 Enterprise image"""

    def __init__(self):
        """
        Initialize the Windows 10 Enterprise instance.

        This sets up the virtual machine (VM) configuration, including architecture,
        virtual CPU (vCPU) settings, memory, drives, and VGA settings. It also sets
        default usernames and passwords for in-experiment images.
        """

        self.vm = getattr(self, "vm", {})

        if "architecture" not in self.vm:
            self.vm["architecture"] = "x86_64"
        if "vcpu" not in self.vm:
            self.vm["vcpu"] = {
                "model": "qemu64",
                "sockets": 1,
                "cores": 1,
                "threads": 1,
            }
        if "mem" not in self.vm:
            self.vm["mem"] = 1024
        if "drives" not in self.vm:
            self.vm["drives"] = [
                {
                    "db_path": "windows-server-2012-r2.qc2.xz",
                    "file": "windows-server-2012-r2.qc2",
                }
            ]
        if "vga" not in self.vm:
            self.vm["vga"] = "std"

        self.set_image("windows-server-2012-r2")

        # Default usernames/passwords for in-experiment images
        # These should be changed depending on unique requirements
        self.user = "Administrator"  # noqa: S105
        self.password = "changeme&1"  # noqa: S105
