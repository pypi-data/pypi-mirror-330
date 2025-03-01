import netaddr
from base_objects import VMEndpoint, AbstractWindowsEndpoint

from firewheel.control.experiment_graph import require_class
from firewheel.vm_resource_manager.schedule_entry import ScheduleEntry


@require_class(VMEndpoint)
@require_class(AbstractWindowsEndpoint)
class WindowsHost:
    """
    This class provides functionality that is common to most Windows hosts, regardless of the version.
    """

    def __init__(self, name=None):
        """
        Initialize the Windows Host.

        Args:
            name (str): The hostname of the VM.

        Raises:
            ValueError: If the Windows Host does not have a name.
        """
        self.type = "host"
        self.name = getattr(self, "name", name)
        if self.name is None:
            raise ValueError("VMEndpoint must have a name!")

        self.rearm_windows()
        self.set_hostname()

    def run_powershell(self, start_time, script_name, arguments=None):
        """
        Creates a :py:class:`PowershellScheduleEntry`.

        Args:
            start_time (int): The time at which to run the script.
            script_name (str): The name of the PowerShell script to run.
            arguments (str or list, optional): Any arguments to provide to the script. Default is None.

        Returns:
            PowershellScheduleEntry: The created PowerShell schedule entry.
        """
        vm_resource = None
        for decorator in self.decorators:
            if "windows_7" in decorator.__module__ or "2008" in decorator.__module__:
                vm_resource = PowershellScheduleEntry(
                    start_time, script_name, arguments, batch=True
                )
                break

        if not vm_resource:
            vm_resource = PowershellScheduleEntry(
                start_time, script_name, arguments, batch=False
            )

        self.vm_resource_schedule.add_vm_resource(vm_resource)
        return vm_resource

    def join_domain(self, domain_id, domain_name, dns=None):
        """
        Joins the Windows host to a domain.

        Args:
            domain_id (str): The domain ID.
            domain_name (str): The domain name.
            dns (str, optional): The DNS server address. Default is None.
        """

        self.windows_domain = getattr(self, "windows_domain", {})
        self.windows_domain["id"] = domain_id
        self.windows_domain["name"] = domain_name
        self.windows_domain["dns"] = dns

    def rearm_windows(self, start_time=-1000):
        """
        Rearms the Windows activation.

        Args:
            start_time (int): The time at which to run the script. Default is -1000.
        """
        self.run_powershell(start_time, "rearm_windows.ps1")

    def set_hostname(self, start_time=-250):
        """
        Sets the hostname of the Windows host.

        Args:
            start_time (int): The time at which to run the script. Default is -250.
        """
        arguments = "-hostname %s" % self.name
        self.run_powershell(start_time, "set_hostname.ps1", arguments)

    def enable_file_sharing(self, start_time=-10):
        """
        Enables file sharing on the Windows host.

        Args:
            start_time (int): The time at which to run the script. Default is -10.
        """
        self.run_powershell(start_time, "enable_file_sharing.ps1")

    def autologon(self, start_time, username, password, domain=None):
        """
        Configures autologon for the Windows host.

        Args:
            start_time (int): The time at which to run the script.
            username (str): The username for autologon.
            password (str): The password for autologon.
            domain (str, optional): The domain for autologon. Default is None.
        """
        if domain:
            arguments = "-Username {} -Password {} -Domain {}".format(
                username, password, domain
            )
        else:
            arguments = "-Username {} -Password {}".format(username, password)

        self.run_powershell(start_time, "autologon.ps1", arguments)

    def remove_autologon(self, start_time):
        """
        Removes autologon configuration from the Windows host.

        Args:
            start_time (int): The time at which to run the script.
        """
        self.run_powershell(start_time, "remove_autologon.ps1")

    def disable_smbv1(self, start_time=-99):
        """
        Disables SMBv1 on the Windows host.

        Args:
            start_time (int): The time at which to run the script. Default is -99.
        """
        self.run_powershell(start_time, "disable_smbv1.ps1")

    def add_ews(self):
        """
        Adds the EWS Managed API to the Windows host.
        """
        resource = self.run_executable(
            -20, "msiexec.exe", "/i EwsManagedApi.msi LICENSE_ACCEPTED=1 /qn"
        )
        resource.add_file("EwsManagedApi.msi", "EwsManagedApi.msi")

    def check_email(
        self, username, password, domain, mailbox, smtp, click_rate, trusted_sender
    ):
        """
        Checks email using the Exchange Web Service (EWS) Managed API.

        Args:
            username (str): The username for email access.
            password (str): The password for email access.
            domain (str): The domain for email access.
            mailbox (str): The mailbox to check.
            smtp (str): The SMTP server address.
            click_rate (int): The click rate for email checking.
            trusted_sender (str): The trusted sender address.
        """
        self.add_ews()
        arguments = str(
            f"-username {username} -password {password} "
            f"-domain {domain} -mailbox {mailbox} "
            f"-smtp {smtp} -clickRate {click_rate} "
            f"-trusted {trusted_sender}"
        )
        self.run_powershell(1, "check_email.ps1", arguments)

    def create_smb_share(
        self, start_time, name, path, caching_mode, folder_enumeration_mode, full_access
    ):
        """
        Creates a Server Message Block (SMB) share on the Windows host.

        Args:
            start_time (int): The time at which to run the script.
            name (str): The name of the SMB share.
            path (str): The path of the SMB share.
            caching_mode (str): The caching mode for the SMB share.
            folder_enumeration_mode (str): The folder enumeration mode for the SMB share.
            full_access (str): The full access permissions for the SMB share.
        """
        self.run_powershell(
            start_time,
            "create_smb_share.ps1",
            "-Name {} -Path {} -CachingMode {} -FolderEnumerationMode {} -FullAccess {}".format(
                name, path, caching_mode, folder_enumeration_mode, full_access
            ),
        )

    def grant_smb_access(self, start_time, name, account):
        """
        Grants access to an SMB share on the Windows host.

        Args:
            start_time (int): The time at which to run the script.
            name (str): The name of the SMB share.
            account (str): The account to grant access to.
        """
        self.run_powershell(
            start_time,
            "grant_smb_access.ps1",
            "-Name {} -Account {}".format(name, account),
        )

    def enable_rdp(self, start_time):
        """
        Enables Remote Desktop Protocol (RDP) on the Windows host.

        Args:
            start_time (int): The time at which to run the script.
        """
        self.run_powershell(start_time, "enable_rdp.ps1")

    def sysprep(self, start_time=-10000):
        """
        Runs the Sysprep tool on the Windows host.

        Args:
            start_time (int): The time at which to run the script. Default is -10000.
        """
        self.run_powershell(start_time, "sysprep.ps1")

    def configure_ips(self, start_time=-200):
        """
        Configures IP addresses on the Windows host.

        Args:
            start_time (int): The time at which to run the script. Default is -200.

        Returns:
            bool: True if IP addresses were configured, False otherwise.
        """
        if getattr(self, "interfaces", None) is None:
            return False

        try:
            nameservers = self.dns_nameservers
            if isinstance(nameservers, list):
                nameservers = " ".join(nameservers)
        except AttributeError:
            nameservers = ""

        config = ""
        for iface in self.interfaces.interfaces:
            if "mac" in iface and "address" in iface and "netmask" in iface:
                # Windows requires a full netmask string (e.g. 255.255.255.0) rather than CIDR (e.g. 24).
                netmask = netaddr.IPNetwork(f"0.0.0.0/{iface['netmask']}").netmask
                config += "%s %s %s" % (iface["mac"], iface["address"], netmask)

                # Add default gateway if there is one
                gateway = getattr(self, "default_gateway", None)
                if gateway and not iface["control_network"]:
                    config += f" {gateway}"
                else:
                    config += " None"

                # Ideally, if this host is in a domain, than its DNS server would be the domain controller.
                # When the host joins the domain its DNS server address will get overridden by
                # the domain controller itself (so essentially this code might be moot in many cases).
                # However, it also isn't guaranteed that the domain controller is itself running a
                # DNS server since that's optional when building a domain (you have to run a
                # DNS server somewhere, but it doesn't strictly have to be colocated on the
                # domain controller). Therefore, this code will remain in case anyone that needs a
                # deeper level of control. We recommend creating a new model component that overrides
                # any DNS/domain parameters.
                try:
                    nameserver = self.dns_nameservers
                    config += " %s" % nameserver
                except AttributeError:
                    config += " None"

                config += "\n"

        config = "%s\n%s" % (nameservers, config)
        vm_resource = self.run_powershell(start_time, "configure_ips.ps1")
        vm_resource.add_dynamic_content("ips.txt", config, "-ips")

        return True

    def wget(self, start_time, address, href_filter=None):
        """
        Downloads a file using wget on the Windows host.

        Args:
            start_time (int): The time at which to run the script.
            address (str): The URL to download.
            href_filter (str, optional): A filter for the href attribute. Default is None.
        """
        arguments = "-address {}".format(address)
        if href_filter:
            arguments += " -filter {}".format(href_filter)
        self.run_powershell(start_time, "wget.ps1", arguments)

    def smb_traffic_gen(self, start_time, share, username, password):
        """
        Generates SMB traffic on the Windows host.

        Args:
            start_time (int): The time at which to run the script.
            share (str): The SMB share to use.
            username (str): The username for SMB access.
            password (str): The password for SMB access.
        """
        self.drop_file(
            start_time - 1, "/launch/smb_traffic_gen.ps1", "smb_traffic_gen.ps1"
        )
        self.run_powershell(
            start_time,
            "run_smb_gen.ps1",
            "-filepath /launch/smb_traffic_gen.ps1 -share {} -username {} -password {}".format(
                share, username, password
            ),
        )
        self.run_powershell(
            1,
            "run_task.ps1",
            "-name SMB{}{}".format(share.split(".")[1], share.split("\\")[-1]),
        )

    def manage_network_share(self, start_time, share, max_files):
        """
        Manages a network share on the Windows host.

        Args:
            start_time (int): The time at which to run the script.
            share (str): The network share to manage.
            max_files (int): The maximum number of files to manage.
        """
        arguments = "-share {} -max {}".format(share, max_files)
        self.run_powershell(start_time, "manage_network_share.ps1", arguments)

    def add_remote_desktop_user(self, start_time, username):
        """
        Adds a user to the Remote Desktop Users group on the Windows host.

        Args:
            start_time (int): The time at which to run the script.
            username (str): The username to add.
        """
        self.run_executable(
            start_time, "add_remote_desktop_user.bat", username, vm_resource=True
        )

    def add_sysinternals(self, start_time):
        """
        Adds Sysinternals tools to the Windows host.

        Args:
            start_time (int): The time at which to run the script.
        """
        self.drop_file(start_time, "/PSTools.zip", "PSTools.zip")

    def change_password(self, start_time, username, password):
        """
        Changes the password for a user on the Windows host.

        Args:
            start_time (int): The time at which to run the script.
            username (str): The username for which to change the password.
            password (str): The new password.
        """
        arguments = "-username {} -password {}".format(username, password)
        self.run_powershell(start_time, "change_password.ps1", arguments)

    def cleanup(self, start_time=1):
        """
        Cleans up the Windows host.

        Args:
            start_time (int): The time at which to run the script. Default is 1.
        """
        self.run_powershell(start_time, "cleanup.ps1")


class PowershellScheduleEntry(ScheduleEntry):
    """
    This class creates a Powershell Schedule Entry.
    This helps run Powershell scripts on various versions of Windows.
    """

    def __init__(self, start_time, powershell_script, arguments=None, batch=False):
        """
        Initialization for a PowershellScheduleEntry.

        Args:
            start_time (int): The time at which to run the script.
            powershell_script (str): The name of the PowerShell script to run.
            arguments (str or list, optional): Any arguments to provide to the script.
                Default is :py:data:`None`.
            batch (bool): Whether or not the default shell is batch and needs to be wrapped to
                run as PowerShell. Default is :py:data:`False`.

        Raises:
            TypeError: If the arguments are not a string nor a list.
        """
        super().__init__(start_time)

        full_argument = powershell_script

        if arguments:
            if isinstance(arguments, list):
                arguments = " ".join(arguments)
            elif not isinstance(arguments, str):
                raise TypeError(
                    "PowershellScheduleEntry takes arguments as a string or a list"
                )

            full_argument += " %s" % arguments

        self.add_file(powershell_script, powershell_script)
        if batch:
            self.add_file("powershell_wrapper.exe", "powershell_wrapper.exe")
            self.set_executable("powershell_wrapper.exe", full_argument)
        else:
            self.set_executable(
                "powershell", "-ExecutionPolicy Bypass -File %s" % full_argument
            )

    def add_dynamic_content(self, target_filename, content, ps_parameter=None):
        """
        Adds dynamic content to the PowerShell schedule entry.

        Args:
            target_filename (str): The target filename for the content.
            content (str): The content to add.
            ps_parameter (str, optional): The PowerShell parameter for the content.
                Default is :py:data:`None`.
        """
        self.add_content(target_filename, content)
        parameter = ""
        if ps_parameter:
            parameter += "%s " % ps_parameter
        parameter += target_filename
        self.append_arguments(parameter)
