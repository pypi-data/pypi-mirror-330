.. _windows.domain_controller_mc:

#########################
windows.domain_controller
#########################

This model component provides functionality for managing a Windows domain controller.
It includes methods for setting up a domain controller, adding and managing users and groups, configuring organizational units (OUs), and establishing trust relationships with remote forests.

The following VM resources are provided with this model component:

1. **join_windows_domain.ps1** - Joins a Windows machine to a specified domain.
2. **install_domain_controller.ps1** - Installs and configures a domain controller on a Windows Server VM.
3. **change_password.ps1** - Changes the password for a specified user.
4. **add_activedirectory_users.ps1** - Adds or updates Active Directory users.
5. **add_OU.ps1** - Adds an Organizational Unit (OU) to Active Directory.
6. **add_ad_group.ps1** - Adds a group to Active Directory.
7. **add_ad_user_to_group.ps1** - Adds a user to a group in Active Directory.
8. **add_domain_site_subnet.ps1** - Adds a replication site and subnet to Active Directory.
9. **add_users_to_adgroup.ps1** - Adds users to an Active Directory group.
10. **create_bidirectional_trust.ps1** - Adds a bidirectional trust relationship with a remote forest.
11. **create_conditional_forwarder.bat** - Adds a conditional forwarder to the DNS server.
12. **join_child_windows_domain.ps1** - Joins a child domain to the domain controller.
13. **move_ad_objects.ps1** - Moves Active Directory objects to a different Organizational Unit (OU).
14. **remove_ad_user.ps1** - Removes a user from Active Directory.
15. **remove_domain_site_subnet.ps1** - Removes a replication subnet from Active Directory.
16. **reset_trust.ps1** - Resets the trust relationship with a remote forest.


*****************
Available Objects
*****************

.. automodule:: windows.domain_controller
    :members:
    :undoc-members:
    :special-members:
    :private-members:
    :show-inheritance:
    :exclude-members: __dict__,__weakref__,__module__

