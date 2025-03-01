.. _windowstests.domain_mc:

###################
windowstests.domain
###################

This Model Component contains a simple plugin that creates a Domain Controller and a specified number of hosts, all connected by a single switch
The Domain Controller is a :py:class:`WindowsServer2008R2 <windows.windows_server_2008_r2.WindowsServer2008R2>` VM.
The hosts are :py:class:`Windows7Enterprise <windows.windows_7_enterprise.Windows7Enterprise>` VMs.
All VMs in this topology will have IP addresses in the ``192.168.150.0/24`` space.

**Attribute Depends:**
    * ``graph``

**Attribute Provides:**
    * ``topology``

**Model Component Dependencies:**
    * :ref:`base_objects_mc`
    * :ref:`windows.windows_7_enterprise_mc`
    * :ref:`windows.windows_server_2008_r2_mc`
    * :ref:`windows.domain_controller_mc`

******
Plugin
******

.. automodule:: windowstests.domain_plugin
    :members:
    :undoc-members:
    :special-members:
    :private-members:
    :show-inheritance:
    :exclude-members: __dict__,__weakref__,__module__
