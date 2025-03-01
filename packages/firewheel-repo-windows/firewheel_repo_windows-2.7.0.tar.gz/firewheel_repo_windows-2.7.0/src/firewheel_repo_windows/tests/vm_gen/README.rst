.. _windowstests.vm_gen_mc:

###################
windowstests.vm_gen
###################

This is very similar to :ref:`tests.vm_gen_mc`, but uses Windows hosts instead of Linux.
This MC will create an arbitrary number of :py:class:`Windows7Enterprise <windows.windows_7_enterprise.Windows7Enterprise>` VMs.
The user can pass in the number as the parameter to the Plugin.
The new VMs will be give the name ``server-X`` where ``X`` is an incrementing integer.

**Attribute Depends:**
    * ``graph``

**Attribute Provides:**
    * ``topology``

**Model Component Dependencies:**
    * :ref:`base_objects_mc`
    * :ref:`windows.windows_7_enterprise_mc`

******
Plugin
******

.. automodule:: windowstests.vm_gen_plugin
    :members:
    :undoc-members:
    :special-members:
    :private-members:
    :show-inheritance:
    :exclude-members: __dict__,__weakref__,__module__
