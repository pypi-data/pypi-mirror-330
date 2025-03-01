.. _windowstests.router_tree_mc:

########################
windowstests.router_tree
########################

This MC is very similar to :ref:`tests.router_tree_mc` but uses Windows hosts instead of Linux.
This MC creates a router high-degree tree running OSPF and BGP.
The leaves of the tree are subnets that include a variable number of host endpoints and have a single gateway router.
The routers at the leaf subnets use OSPF to advertise connectivity of their endpoints.
The leaf routers then redistribute their OSPF routes to upstream BGP routers, eventually culminating in the BGP router at the root of the topology tree.
The user *must* pass in a degree for the tree (i.e. the desired number of OSPF branches.)

The following diagram depicts the result of running the router tree topology with a parameter of three::

    <host> -- <OSPF> -- <BGP> -------------------------
                              |           |           |
                           <BGP 0>     <BGP 1>     <BGP 2>
                              |           |           |
                           <OSPF 0>    <OSPF 1>    <OSPF 2>
                              |           |           |
                           <host 0>    <host 1>    <host 2>



This MC primarily serves as part of the functional testing suite and as an example for building complex routed networks using FIREWHEEL.
For more information please see :ref:`router-tree-tutorial`.

**Attribute Provides:**
    * ``topology``

**Attribute Depends:**
    * ``graph``

**Model Component Dependencies:**
    * :ref:`base_objects_mc`
    * :ref:`generic_vm_objects_mc`
    * :ref:`windows.base_objects_mc`
    * :ref:`windows.windows_7_enterprise_mc`

******
Plugin
******

.. automodule:: windowstests.router_tree_plugin
    :members:
    :undoc-members:
    :special-members:
    :private-members:
    :show-inheritance:
    :exclude-members: __dict__,__weakref__,__module__
