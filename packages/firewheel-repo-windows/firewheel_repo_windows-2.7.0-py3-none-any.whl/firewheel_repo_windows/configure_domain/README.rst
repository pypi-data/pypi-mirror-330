.. _windows.configure_domain_mc:

########################
windows.configure_domain
########################

This MC contains a FIREWHEEL plugin designed to configure and schedule the joining of a domain and the creation of a domain controller.
Additionally, the following VM resources are provided with this model component:

1. **join_windows_domain.ps1** - Joins a Windows machine to a specified domain.
2. **install_domain_controller.ps1** - Installs and configures a domain controller on a Windows Server machine.
3. **change_password.ps1** - Changes the password for a specified user.
4. **add_activedirectory_users.ps1** - Adds or updates Active Directory users.

**Attribute Depends:**
    * ``graph``

**Attribute Provides:**
    * ``windows_domain``

**Model Component Dependencies:**
    * :ref:`windows.base_objects_mc`
    * :ref:`dns.dns_objects_mc`

******
Plugin
******

.. automodule:: windows.configure_domain_plugin
    :members:
    :undoc-members:
    :special-members:
    :private-members:
    :show-inheritance:
    :exclude-members: __dict__,__weakref__,__module__
