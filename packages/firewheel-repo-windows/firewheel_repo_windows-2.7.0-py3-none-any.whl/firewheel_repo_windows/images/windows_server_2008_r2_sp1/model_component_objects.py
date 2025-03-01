from base_objects import AbstractServerEndpoint
from windows.base_objects import WindowsHost

from firewheel.control.experiment_graph import require_class


@require_class(WindowsHost)
@require_class(AbstractServerEndpoint)
class WindowsServer2008R2:
    """The Model Component for the Windows 2008 Server R2 image"""

    def __init__(self):
        """
        Initialize the Windows Server 2008 R2 instance.

        This sets up the virtual machine (VM) configuration, including architecture,
        virtual CPU (vCPU) settings, memory, drives, and VGA settings. It also sets
        default usernames and passwords for in-experiment images.
        """
        self.vm = {
            "architecture": "x86_64",
            "vcpu": {"model": "qemu64", "sockets": 1, "cores": 1, "threads": 1},
            "mem": 1024,
            "drives": [
                {
                    "db_path": "windows-server-2008-r2-sp1.qc2.xz",
                    "file": "windows-server-2008-r2-sp1.qc2",
                }
            ],
            "vga": "std",
        }
        self.set_image("windows-server-2008-r2-sp1")

        # Default usernames/passwords for in-experiment images
        # These should be changed depending on unique requirements
        self.user = "Administrator"  # noqa: S105
        self.password = "changeme&1"  # noqa: S105
