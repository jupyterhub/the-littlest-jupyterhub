.. _howto/providers/azure:

==================================================
Perform common Microsoft Azure configuration tasks
==================================================

This page lists various common tasks you can perform on your
`Microsoft Azure virtual machine <https://azure.microsoft.com/services/virtual-machines/?WT.mc_id=TLJH-github-taallard>`_.

.. _howto/providers/azure/resize:

Deleting or stopping your virtual machine
===========================================

After you have finished using your TLJH you might wanto to either Stop or completely delete the Virtual Machine to avoid incurring in subsequent costs. 

The difference between these two approaches is that **Stop** will keep the VM resources (e.g. storage and network) but will effectively stop any compute / runtime activities. 

If you choose to delete the VM then all the resources associated with it will be wiped out.

To do either of this:

* Go to "Virtual Machines" on the left hand panel
* Click on your machine name
* Click on "Stop" to stop the machine temporarily, or "Delete" to delete it permanently.

    .. image:: ../../images/providers/azure/delete-vm.png
        :alt: Delete vm

.. note:: It is important to mention that even if you stop the machine you will still be charged for the use of the data disk.

If you no longer need any of your resources you can delete the entire resource group.

* Go to "Reosurce groups" on the left hand panel
* Click on your resource group
* Click on "Delete resource group" you will then be asked to confirm the operation.  This operation will take between 5 and 10 minutes.
