.. _windowstests.domain_trusts_mc:

##########################
windowstests.domain_trusts
##########################

This Model Component creates a topology with two Domain Controllers and two Windows hosts.
It then creates a bidirectional trust between the two Domain Controllers.

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

.. automodule:: windowstests.domain_trusts_plugin
    :members:
    :undoc-members:
    :special-members:
    :private-members:
    :show-inheritance:
    :exclude-members: __dict__,__weakref__,__module__
