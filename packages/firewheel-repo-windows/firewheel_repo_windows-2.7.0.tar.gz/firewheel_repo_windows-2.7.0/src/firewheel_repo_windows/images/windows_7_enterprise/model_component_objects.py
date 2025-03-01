from base_objects import AbstractDesktopEndpoint
from windows.base_objects import WindowsHost

from firewheel.control.experiment_graph import require_class


@require_class(WindowsHost)
@require_class(AbstractDesktopEndpoint)
class Windows7Enterprise(object):
    """The Model Component for the Windows 7 Enterprise image"""

    def __init__(self):
        """
        Initialize the Windows 7 Enterprise instance.

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
                    "db_path": "windows-7-enterprise-sp1.qc2.xz",
                    "file": "windows-7-enterprise-sp1.qc2",
                }
            ],
            "vga": "std",
        }
        self.set_image("windows-7-enterprise-sp1")

        # Default usernames/passwords for in-experiment images
        # These should be changed depending on unique requirements
        self.user = "User"  # noqa: S105
        self.password = "user"  # noqa: S105

        self.schedule = getattr(self, "schedule", [])
