from dns.dns_objects import DNSServer
from windows.base_objects import WindowsHost

from firewheel.control.experiment_graph import AbstractPlugin


class ConfigureDomain(AbstractPlugin):
    """
    This plugin configures and schedules joining a domain and creating a domain controller.
    """

    join_rel_time = -50

    def run(self):
        """
        Executes the domain configuration process.

        The logic is as follows:
            - Find all the domain controllers in the graph.
            - Schedule the DC and then find its experiment IP address.
            - Find all vertices (hosts) that belong to that domain and schedule them.
        """
        dc_ip = {}
        for v in self.g.get_vertices():
            if not v.is_decorated_by(WindowsHost):
                continue

            if (
                getattr(v, "windows_domain", None) is not None
                and "controller" in v.windows_domain
                and v.windows_domain["controller"]
            ):
                self.set_dc_schedule(v)

                if getattr(v, "interfaces", None) is None:
                    continue

                # If the address is not 0.0.0.0 or starts with 172 we assume it
                # is the experiment address.
                for interface in v.interfaces.interfaces:
                    if not str(interface["address"]) == "0.0.0.0":  # noqa: S104
                        dc_ip[v.windows_domain["id"]] = {
                            "ip": interface["address"],
                            "dns_name": v.windows_domain["name"],
                        }

        # Needs a separate loop so we know all of the domain controllers.
        for host in self.g.get_vertices():
            if not host.is_decorated_by(WindowsHost):
                continue

            if getattr(host, "windows_domain", None) is None:
                continue

            # Find each host that should join v's domain
            if (
                "id" in host.windows_domain
                and host.windows_domain["id"] is not None
                and (
                    "controller" not in host.windows_domain
                    or host.windows_domain["controller"] is None
                )
            ):
                if host.windows_domain["id"] in dc_ip:
                    self.set_host_schedule(
                        host,
                        dc_ip[host.windows_domain["id"]]["dns_name"],
                        dc_ip[host.windows_domain["id"]]["ip"],
                    )
                else:
                    print(
                        'Error: Domain controller not found for "%s"'
                        % host.windows_domain["name"]
                    )

    def get_dns_address(self):
        """
        Gets the IP address of the DNS Server in the experiment.

        Returns:
            str: The IP address of the DNS server, or None if not found.
        """
        for v in self.g.get_vertices():
            if v.is_decorated_by(DNSServer):
                dns = str(v.dns_data.get("dns_address"))
                if not dns:
                    continue
                return dns

    def set_dc_schedule(self, v):
        """
        Adds to the domain controller's schedule.

        .. warning::

            This method assumes that the Administrator password is originally set to:
            ``changeme&1`` and then changed to ``ChangeThisPassword#1``.
            Users should update this as needed.

        Args:
            v (Vertex): The vertex describing the domain controller.
        """
        # Set up the default NETBIOS name if there isn't already one present.
        if "netbios" not in v.windows_domain or not v.windows_domain["netbios"]:
            v.windows_domain["netbios"] = v.windows_domain["name"].split(".")[0].upper()

        if v.windows_domain.get("upstream_dns"):
            upstream_dns = v.windows_domain["upstream_dns"]
        else:
            upstream_dns = self.get_dns_address()

        # We assume that the ``safe_mode_admin_password`` is ``changeme&1`` initially
        # Default usernames/passwords for in-experiment images are safe to hard-code
        admin_password = "changeme&1"  # noqa: S105
        domain_name = v.windows_domain["name"]
        arguments = "-domain %s -netBiosName %s -safe_mode_admin_password %s" % (
            domain_name,
            v.windows_domain["netbios"],
            admin_password,
        )

        if upstream_dns:
            arguments += " -upstream_dns %s" % upstream_dns

        # If we are using a snapshot version of the DC where things are already set up, we do not
        # need to configure it.
        try:
            if not v.snapshot:
                v.run_powershell(
                    self.join_rel_time, "install_domain_controller.ps1", arguments
                )
        except AttributeError:
            v.run_powershell(
                self.join_rel_time, "install_domain_controller.ps1", arguments
            )

        arguments = "-username administrator -password ChangeThisPassword#1"
        v.run_powershell(self.join_rel_time + 1, "change_password.ps1", arguments)

        self.add_users(v)

    def add_users(self, v):
        """
        Adds users to the domain controller.

        Args:
            v (Vertex): The vertex describing the domain controller.
        """
        if "users" not in v.windows_domain or not v.windows_domain["users"]:
            return

        users = ""
        for user in v.windows_domain["users"]:
            users += "%s %s\n" % (user["username"], user["password"])

        if users:
            vm_resource = v.run_powershell(
                self.join_rel_time + 2, "add_activedirectory_users.ps1"
            )
            vm_resource.add_dynamic_content("users.txt", users, "-Users")

    def set_host_schedule(self, host, domain_dns_name, dc_ip):
        """
        Adds to the hosts' schedule if it is part of a domain.

        .. warning::

            This method assumes that the Administrator password is set to:
            ``ChangeThisPassword#1`` and will need to be updated by users.

        Args:
            host (Vertex): The vertex describing the host.
            domain_dns_name (str): The DNS name used to join the domain.
            dc_ip (str): The experiment IP address of the domain controller.
        """
        arguments = (
            "-domain_name %s -admin_user Administrator "
            "-admin_password ChangeThisPassword#1 -domain_controller_ip %s"
            % (domain_dns_name, dc_ip)
        )
        if host.windows_domain.get("dns"):
            arguments += " -dns_ip {}".format(host.windows_domain["dns"])
        host.run_powershell(self.join_rel_time, "join_windows_domain.ps1", arguments)

    def fix_hostname(self, host):
        """
        Ensures the hostname is set before joining the domain
        regardless of whether anyone else has tried to set the hostname.

        Args:
            host (Vertex): The vertex describing the host.
        """
        host.add_vm_resource(
            self.join_rel_time - 1, "set_hostname.py", host.name.split(".")[0], None
        )
