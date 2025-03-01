.. _windows.utils_mc:

#############
windows.utils
#############

This Model Component contains many basic utilities for windows to help troubleshoot or diagnose issues.
It includes:

* `Sysmon and Sysmon64 <https://docs.microsoft.com/en-us/sysinternals/downloads/sysmon>`_ - A Windows system service and device driver that monitors and logs system activity to the Windows event log.
  It provides detailed information about process creations, network connections, and changes to file creation time.
* `PuTTY <https://www.chiark.greenend.org.uk/~sgtatham/putty/latest.html>`_ - An SSH and Telnet client.
* `pscp <https://www.chiark.greenend.org.uk/~sgtatham/putty/latest.html>`_ - An SCP client.
* `puttygen <https://www.chiark.greenend.org.uk/~sgtatham/putty/latest.html>`_ - A RSA and DSA key generation utility

This MC has a Plugin which installs these tools on each Windows system in the topology.

**Attribute Depends:**
    * ``graph``

**Model Component Dependencies:**
    * :ref:`base_objects_mc`


******
Plugin
******

.. automodule:: windows.utils_plugin
    :members:
    :undoc-members:
    :special-members:
    :private-members:
    :show-inheritance:
    :exclude-members: __dict__,__weakref__,__module__

