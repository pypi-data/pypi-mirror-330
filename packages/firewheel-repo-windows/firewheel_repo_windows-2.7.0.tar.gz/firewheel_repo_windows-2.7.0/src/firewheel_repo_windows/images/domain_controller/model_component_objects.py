class DomainController:
    """
    The DomainController class provides functionality for managing a Windows domain controller.
    """

    def __init__(self, domain_id, domain_name, netbios_name):
        """
        Initialize the Domain Controller.

        Attributes:
            windows_domain (dict): A dictionary of domain-related properties.
                These will be used by other model components to connect VMs to the domain controller
                and ensure proper domain configuration throughout the experiment.
                Properties in this dictionary include:

                -  ``id`` - A unique identifier for this domain. This is used only on the graph
                   so we have unambiguous names for client/controller relationships.
                - ``controller`` - If set to :py:data:`True`, this host will run the
                   VM resource to set up a DC.
                - ``name`` - The DNS name of the Windows domain to join or control.
                - ``netbios`` - The NETBIOS (short, used in usernames, etc.) name for the domain.
                   Only valid on domain controllers, should be ignored on other vertices.
                   If not present, will be set to the first group in the DNS domain name
                   (that is, for ``test.foo.local``, the NETBIOS name would be ``TEST``).

        Args:
            domain_id (str): The domain ID (NetBiosName).
            domain_name (str): The domain name (Domain ID).
            netbios_name (str): The NetBIOS name.
        """
        self.windows_domain = getattr(self, "windows_domain", {})

        self.windows_domain["id"] = domain_id  # NetBiosName
        self.windows_domain["controller"] = True
        self.windows_domain["name"] = domain_name  # Domain ID
        self.windows_domain["netbios"] = netbios_name  # NetBiosName

        self.vm["vcpu"] = {"model": "qemu64", "cores": 8, "sockets": 1, "threads": 1}
        self.vm["mem"] = 8192

    def set_child_domain(self, start_time, domain_dns_name, dc_ip):
        """
        Joins a child domain to the domain controller.

        Args:
            start_time (int): The time at which to run the script.
            domain_dns_name (str): The domain DNS name (e.g., company.com).
            dc_ip (str): The IP address of the Domain Controller.
        """
        arguments = (
            f"-domain_name {domain_dns_name} -admin_user Administrator "
            f"-admin_password ChangeThisPassword#1 -domain_controller_ip {dc_ip}"
        )
        self.run_powershell(start_time, "join_child_windows_domain.ps1", arguments)

    def add_user(self, username, password):
        """
        Adds a user to the domain.

        Args:
            username (str): The username of the user.
            password (str): The password of the user.
        """
        if "user" not in self.windows_domain or not self.windows_domain["users"]:
            self.windows_domain["users"] = []

        user = {"username": username, "password": password}

        self.windows_domain["users"].append(user)

    def add_users(self, users):
        """
        Adds multiple users to the domain.

        Args:
            users (list): A list of dictionaries containing user information.
        """
        if "users" not in self.windows_domain or not self.windows_domain["users"]:
            self.windows_domain["users"] = []

        self.windows_domain["users"].extend(users)

    def remove_ad_user(self, start_time, user):
        """
        Removes a user from Active Directory.

        Args:
            start_time (int): The time at which to run the script.
            user (str): The username of the user to remove.
        """
        self.run_powershell(start_time, "remove_ad_user.ps1", "-name {}".format(user))

    def add_group(self, start_time=-25, group=None, scope="Global"):
        """
        Adds a group to Active Directory.

        Args:
            start_time (int): The time at which to run the script. Default is -25.
            group (str, optional): The name of the group. Default is None.
            scope (str): The scope of the group. Default is "Global".
        """
        if group is None:
            return
        self.run_powershell(
            start_time, "add_ad_group.ps1", f"-group {group} -scope {scope}"
        )

    def add_users_to_group(self, start_time=-23, users=None, group=None):
        """
        Adds users to an Active Directory group.

        Args:
            start_time (int): The time at which to run the script. Default is -23.
            users (list, optional): A list of usernames to add. Default is None.
            group (str, optional): The name of the group. Default is None.
        """
        if users is None or group is None:
            return
        self.run_powershell(
            start_time,
            "add_users_to_adgroup.ps1",
            "-users {} -group '{}'".format(users, group),
        )

    def add_ou(self, start_time=-20, name=None, path=None):
        """
        Adds an Organizational Unit (OU) to Active Directory.

        Args:
            start_time (int): The time at which to run the script. Default is -20.
            name (str, optional): The name of the OU (e.g., "Workstations"). Default is None.
            path (str, optional): The path of the OU (e.g., "DC=acme,DC=com"). Default is None.
        """
        if name is None or path is None:
            return
        self.run_powershell(
            start_time, "add_OU.ps1", "-name {} -path {}".format(name, path)
        )

    def move_user(self, start_time, username, group):
        """
        Moves a user into a group in Active Directory.

        Args:
            start_time (int): The time at which to run the script.
            username (str): The username of the user.
            group (str): The name of the group.
        """
        self.run_powershell(
            start_time,
            "add_ad_user_to_group.ps1",
            "-username {} -group {}".format(username, group),
        )

    def add_ad_replication_site(self, start_time, site, subnet):
        """
        Adds a replication site and subnet to Active Directory.

        Args:
            start_time (int): The time at which to run the script.
            site (str): The name of the replication site.
            subnet (str): The subnet for the replication site.
        """
        self.run_powershell(
            start_time, "add_domain_site_subnet.ps1", f"-site {site} -subnet {subnet}"
        )

    def remove_ad_replication_subnet(self, start_time, subnet):
        """
        Removes a replication subnet from Active Directory.

        Args:
            start_time (int): The time at which to run the script.
            subnet (str): The subnet to remove.
        """
        self.run_powershell(
            start_time, "remove_domain_site_subnet.ps1", f"-subnet {subnet}"
        )

    def move_ad_objects(self, start_time, ou_group, endpoints, domain):
        """
        Moves Active Directory objects to a different Organizational Unit (OU).

        Args:
            start_time (int): The time at which to run the script.
            ou_group (str): The name of the OU group.
            endpoints (list): A list of endpoints to move.
            domain (str): The domain name.
        """
        identity = ""
        for element in domain.split("."):
            identity += "DC=%s," % element
        identity = identity.strip(",")

        objects = ""
        for endpoint in endpoints:
            objects += "CN={},CN=Computers,{} OU={},{}\n".format(
                endpoint.name.split(".")[0], identity, ou_group, identity
            )

        ps = self.run_powershell(start_time, "move_ad_objects.ps1")
        ps.add_dynamic_content("objects.txt", objects, ps_parameter="-Filename")

    def add_conditional_forwarder(self, start_time, zone, ip):
        """
        Adds a conditional forwarder to the DNS server.

        Args:
            start_time (int): The time at which to run the script.
            zone (str): The DNS zone.
            ip (str): The IP address of the forwarder.
        """
        self.run_executable(
            start_time,
            "create_conditional_forwarder.bat",
            f"{zone} {ip}",
            vm_resource=True,
        )

    def add_bidirectional_trust(
        self, start_time, remote_forest_name, remote_username, remote_password
    ):
        """
        Adds a bidirectional trust relationship with a remote forest.

        Args:
            start_time (int): The time at which to run the script.
            remote_forest_name (str): The name of the remote forest.
            remote_username (str): The username for the remote forest.
            remote_password (str): The password for the remote forest.
        """
        arguments = "-remoteForestName {} -remoteUser {} -remotePassword {}".format(
            remote_forest_name, remote_username, remote_password
        )
        self.run_powershell(start_time, "create_bidirectional_trust.ps1", arguments)

    def add_inbound_trust(
        self, start_time, remote_forest_name, remote_username, remote_password
    ):
        """
        Adds an inbound trust relationship with a remote forest.

        Args:
            start_time (int): The time at which to run the script.
            remote_forest_name (str): The name of the remote forest.
            remote_username (str): The username for the remote forest.
            remote_password (str): The password for the remote forest.
        """
        arguments = "-remoteForestName {} -remoteUser {} -remotePassword {}".format(
            remote_forest_name, remote_username, remote_password
        )
        self.run_powershell(start_time, "create_inbound_trust.ps1", arguments)

    def reset_trust(
        self,
        start_time,
        local_forest_name,
        remote_forest_name,
        remote_username,
        remote_password,
    ):
        """
        Resets the trust relationship with a remote forest.

        Args:
            start_time (int): The time at which to run the script.
            local_forest_name (str): The name of the local forest.
            remote_forest_name (str): The name of the remote forest.
            remote_username (str): The username for the remote forest.
            remote_password (str): The password for the remote forest.
        """
        arguments = "-localForestName {} -remoteForestName {} -remoteUser {} -remotePassword {}".format(
            local_forest_name, remote_forest_name, remote_username, remote_password
        )
        self.run_powershell(start_time, "reset_trust.ps1", arguments)

    def add_local_bidirectional_trust(
        self, start_time, remote_forest_name, trust_password
    ):
        """
        Adds a local bidirectional trust relationship with a remote forest.

        Args:
            start_time (int): The time at which to run the script.
            remote_forest_name (str): The name of the remote forest.
            trust_password (str): The trust password.
        """
        arguments = "-remoteForestName {} -trustPassword '{}'".format(
            remote_forest_name, trust_password
        )
        self.run_powershell(start_time, "create_bidirectional_trust.ps1", arguments)
