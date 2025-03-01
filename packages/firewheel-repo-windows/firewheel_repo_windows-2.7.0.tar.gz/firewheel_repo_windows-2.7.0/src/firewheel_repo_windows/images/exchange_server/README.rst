.. _windows.windows.exchange_server_mc:

#######################
windows.exchange_server
#######################

This model component provides functionality for managing an Exchange Server running on Windows Server 2012 R2.
It includes methods for installing Exchange Server, adding mailboxes, and preparing the server for Exchange installation.

The following VM resources are provided with this model component:

1. **add_mailboxes.ps1** - Adds mailboxes for users on the Exchange Server.
2. **install_exchange_server.ps1** - Installs Microsoft Exchange Server on the VM.
3. **prep_exchange.ps1** - Prepares the Windows Server for Exchange installation by installing required features.
4. **run_add_mailboxes.ps1** - Executes the script to add mailboxes using PsExec.
5. **run_exchange_installation.ps1** - Executes the Exchange Server installation script using PsExec.


**Model Component Dependencies:**
    * :ref:`windows.windows_server_2012_r2_mc`

*****************
Available Objects
*****************

.. automodule:: windows.exchange_server
    :members:
    :undoc-members:
    :special-members:
    :private-members:
    :show-inheritance:
    :exclude-members: __dict__,__weakref__,__module__

