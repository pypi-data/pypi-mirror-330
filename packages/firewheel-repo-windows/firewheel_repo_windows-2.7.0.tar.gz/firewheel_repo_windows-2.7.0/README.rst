.. _windows_mc_repo:

**********************
firewheel_repo_windows
**********************

This repository contains FIREWHEEL Model Components related to Microsoft Windows and Windows specific applications.
Currently, there are generic Windows-related MCs as well as MCs related to several Windows versions.

Building Images and VMRs
========================

Due to licensing limitations, we are currently unable to provide the expected binary files (VM Resources nor Images) that are used within these model components.
For the VM Resources, we have provided an `INSTALL <https://sandialabs.github.io/firewheel/tutorials/install_file.html>`__ script to reproducibly recreate them, when possible.
However, for images, users will need to follow the `Image Creation Tutorial <https://sandialabs.github.io/firewheel/tutorials/image.html>`__ to create compatible images.

.. note::

    To download and subsequently use Windows images, users will need a `Visual Studio Subscription <https://visualstudio.microsoft.com/subscriptions/>`__.
    We strongly advise consulting with a legal expert or attorney prior to use of any licensed product within an Emulytics experiment to ensure compliance with the applicable licensing terms.

The following images are referenced within this repository:

Located in ``windows.windows_7_enterprise_mc``
----------------------------------------------
- `Windows 7 Enterprise SP1 <https://support.microsoft.com/en-us/topic/update-to-windows-7-sp1-for-performance-improvements-f6469085-6dc4-59ef-3102-8d515e67651a>`_


Located in ``windows.windows_10_enterprise_mc``
-----------------------------------------------
- `Windows 10 Enterprise <https://www.microsoft.com/en-us/software-download/windows10ISO>`_


Located in ``windows.windows_server_2008_r2_mc``
------------------------------------------------
- `Windows Server 2008 R2 SP1 <https://support.microsoft.com/en-us/topic/information-about-service-pack-1-for-windows-7-and-for-windows-server-2008-r2-df044624-55b8-3a97-de80-5d99cb689063>`_


Located in ``windows.windows_server_2012_r2_mc``
------------------------------------------------
- `Windows Server 2012 R2 <https://www.microsoft.com/en-us/evalcenter/evaluate-windows-server-2012-r2>`_