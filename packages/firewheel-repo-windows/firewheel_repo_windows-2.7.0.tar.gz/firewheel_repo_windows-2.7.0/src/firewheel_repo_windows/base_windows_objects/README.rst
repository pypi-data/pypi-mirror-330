.. _windows.base_objects_mc:

####################
windows.base_objects
####################

This Model Component provides some base objects that are often needed for Windows Model Components.
Notably, this provides :py:class:`PowershellScheduleEntry` which helps run PowerShell scripts on a VM.

The following VM resources are provided with this model component:

1. **add_remote_desktop_user.bat** - Adds a user to the Remote Desktop Users group.
2. **autologon.ps1** - Configures autologon for a specified user.
3. **change_password.ps1** - Changes the password for a specified user.
4. **check_email.ps1** - Checks email using the EWS Managed API.
5. **cleanup.ps1** - Cleans up files in the ``C:\\launch`` directory (which are put there by FIREWHEEL).
6. **configure_ips.ps1** - Configures IP addresses on the Windows host.
7. **create_smb_share.ps1** - Creates an SMB share on the Windows host.
8. **disable_smbv1.ps1** - Disables SMBv1 on the Windows host.
9. **enable_file_sharing.ps1** - Enables file sharing on the Windows host.
10. **enable_rdp.ps1** - Enables Remote Desktop Protocol (RDP) on the Windows host.
11. **grant_smb_access.ps1** - Grants access to an SMB share on the Windows host.
12. **manage_network_share.ps1** - Manages a network share on the Windows host.
13. **rearm_windows.ps1** - Rearms the Windows activation.
14. **remove_autologon.ps1** - Removes autologon configuration from the Windows host.
15. **run_smb_gen.ps1** - Registers and modifies a scheduled task to generate SMB traffic.
16. **run_task.ps1** - Starts a scheduled task.
17. **set_hostname.ps1** - Sets the hostname of the Windows host.
18. **smb_traffic_gen.ps1** - Generates SMB traffic on the Windows host.
19. **wget.ps1** - Downloads a file using wget on the Windows host.


**Model Component Dependencies**:
    * :ref:`base_objects_mc`

*****************
Available Objects
*****************

.. automodule:: windows.base_objects
    :members:
    :undoc-members:
    :special-members:
    :private-members:
    :show-inheritance:
    :exclude-members: __dict__,__weakref__,__module__

