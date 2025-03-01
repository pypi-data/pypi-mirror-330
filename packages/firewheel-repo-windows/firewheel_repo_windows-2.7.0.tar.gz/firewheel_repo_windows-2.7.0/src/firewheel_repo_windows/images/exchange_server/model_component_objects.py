from windows.windows_server_2012_r2 import WindowsServer2012R2

from firewheel.control.experiment_graph import require_class


@require_class(WindowsServer2012R2)
class ExchangeServer:
    """
    The Model Component for the Exchange Server running on Windows Server 2012 R2.
    """

    def __init__(self):
        """
        Initialize the Exchange Server instance.

        This sets up the virtual machine (VM) configuration, including virtual CPU (vCPU)
        settings and memory.
        """
        self.snapshot = getattr(self, "snapshot", False)

        self.vm = getattr(self, "vm", {})

        self.vm["vcpu"] = {"model": "qemu64", "sockets": 1, "cores": 4, "threads": 1}
        self.vm["mem"] = 8092

    def install_exchange(
        self, start_time, username, password, domain_controller, org_name
    ):
        """
        Installs Microsoft Exchange Server on the VM.

        Args:
            start_time (int): The time at which to start the installation process.
            username (str): The username for autologon.
            password (str): The password for autologon.
            domain_controller (str): The domain controller to use.
            org_name (str): The organization name for the Exchange Server.
        """
        self.run_powershell(-46, "prep_exchange.ps1")
        self.run_executable(
            -45, "NDP452-KB2901907-x86-x64-AllOS-ENU.exe", "/q", vm_resource=True
        )

        # Drop the exchange zip file with the installer
        exchange_zip = "/launch/exchange_server.zip"
        self.drop_file(-100, exchange_zip, "exchange_server.zip")
        # Drop the installer PowerShell script
        installer_path = "/launch/install_exchange_server.ps1"
        self.drop_file(-100, installer_path, "install_exchange_server.ps1")
        self.drop_file(-99, "/launch/UcmaRuntimeSetup.exe", "UcmaRuntimeSetup.exe")

        self.autologon(start_time - 1, username, password)
        arguments = str(
            f"-username {username} -password {password} "
            f"-installerPath {installer_path} -exchangeZip {exchange_zip} "
            f"-domainController {domain_controller} -orgName {org_name}"
        )
        self.run_powershell(start_time, "run_exchange_installation.ps1", arguments)

    def add_mailboxes(self, users, username, password, domain=None):
        """
        Adds mailboxes for users on the Exchange Server.

        Args:
            users (list): A list of usernames or dictionaries containing user information.
            username (str): The username for autologon.
            password (str): The password for autologon.
            domain (str, optional): The domain name. Default is None.
        """
        formatted_users = ""
        for user in users:
            if isinstance(user, str):
                if domain:
                    formatted_users += "{}\\".format(domain)
                formatted_users += "{}\n".format(user)
            elif isinstance(user, dict) and "username" in user:
                if domain:
                    formatted_users += "{}\\".format(domain)
                formatted_users += "{}\n".format(user["username"])

        if formatted_users:
            self.add_sysinternals(-11)
            self.autologon(-10, username, password, domain)
            self.drop_file(-25, "/launch/add_mailboxes.ps1", "add_mailboxes.ps1")
            self.drop_content(-24, "/launch/mailbox_users.txt", formatted_users)
            if domain:
                username = "{}\\{}".format(domain, username)
            self.run_powershell(
                -5,
                "run_add_mailboxes.ps1",
                f"-path C:\\launch\\add_mailboxes.ps1 -username {username}"
                f" -password {password} -hostname {self.name}"
                " -users C:\\launch\\mailbox_users.txt"
                " -pstools {}".format(r"C:\PSTools.zip"),
            )
