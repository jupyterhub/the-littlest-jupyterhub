====================
Installing on Azure
====================

Goal
====

By the end of this tutorial, you should have a JupyterHub with some admin
users and a user environment with packages you want installed running on
`Microsoft Azure <https://azure.microsoft.com>`_.

Prerequisites
==============

* A Microsoft Azure account. 

* To get started you can get a free acount which  includes 150 dollars worth of Azure acredits (`get a free account here <https://azure.microsoft.com/en-us/free//?wt.mc_id=LTJH-github-taallard>`_) 

These instructions cover how to set up a Virtual Machine
on Microsoft Azure. For subsequent information about creating
your JupyterHub and configuring it, see `The Littlest JupyterHub guide <https://the-littlest-jupyterhub.readthedocs.io/en/latest/>`_.

Choose your Virtual Machine operating system
=============================================

#. Go to `your azure portal <https://portal.azure.com/>`_ 
#. Find virtual machines on your Azure dashboard (left hand panel)

    .. image:: ../images/providers/azure/azure-vms.png
            :alt: Virtual machines on Azure portal

#. Click "+ add" to create a new Virtual Machine

    .. image:: ../images/providers/azure/add-vm.png
        :alt: Add a new virtual machine

#. Select Create VM from Marketplace
    .. image:: ../images/providers/azure/create-vm.png
        :alt: Create from marketplace
  
* **Choose an Ubuntu server for your VM**.
    * Click `Ubuntu Server`
    * Click `Ubuntu Server 18.04 LTS`
    * Make sure `Resource Manager` is selected when creating the virtual machine

    .. image:: ../images/providers/azure/ubuntu-vm.png
        :alt: Ubuntu VM

Customize the virtual machine
==============================

* Basics
    * **Name**. Use a descriptive, short name that you like (note that you cannot use spaces or special characters)
    * **VM disk type**. Choose SSD
    * **Username**. Choose any username. This will be used to SSH into your VM, it is the root username for your VM.
    * **Authentication type**. Change authentication type to "password"
    * **Password**. Type in a password. This will be used to SSH into the machine. It is your user password on the VM.
    * **Login with Azure Active Directory**. Choose "Disabled" (usually the default)
    * **Subscription**. Choose the "Free Trial" if this is what you're using. Otherwise choose a different plan. This is the billing account that will be charged.
    * **Resource group**. Create new resource group if you don't already have one. Resource groups let you bundle components that you request from Azure. This is overkill for our use case so it's easiest to create a new resource group.
    * **Location**. Choose a location near where you expect your users to be located.

    .. image:: ../images/providers/azure/password-vm.png
            :alt: Add password to vm

* Size
    * Choose a machine with enough RAM to accomodate your users. For example, if each user needs 2GB of RAM, and you have 10 total users, you need at least 20GB of RAM on the machine. It's also good to have a few GB of "buffer" RAM beyond what you think you'll need.
    * Click on "select image" and choose one of the options, then click "select".
    
    .. image:: ../images/providers/azure/size-vm.png
            :alt: Choose vm size 
    

* Settings
    * High Availability
        * **Availability zone**. Make sure "None" is selected.
        * **Availability set**. Make sure "None" is selected.
    * Storage
        * **Use managed disks**. Choose "yes"
        * **OS disk size**. Select the appropriate size for your JupyterHub.
    * Network
        * **Virtual network**. Do not change this.
        * **Subnet**. Do not change this.
        * **Public IP address**. Do not change this.
        * **Network Security Group**. Choose "Basic"
        * **Select public inbound ports**. Check "HTTP", "HTTPS", and "SSH".
    * Extensions
        * **Extensions**. Should read "No extensions".
    * Auto-Shutdown
        * **Enable auto-shutdown**. Choose "Off".
    * Monitoring
        * **Boot diagnostics**. Choose "Enabled".
        * **Guest OS diagnostics**. Choose "Disabled".
        * **Diagnostics storage account**. Leave as teh default.
    * Managed service identity
        * **Register with Azure Active Directory**. Choose "No".
    * Backup
        * **Backup**. Choose "Disabled".
  
.. image:: ../images/providers/azure/backup-vm.png
            :alt: Choose vm Backup


* Summary -> confirm -> OK

  ![](https://i.imgur.com/VNEOnHA.png)

* Confirm that it worked
    * Wait for it to be created. Should take about 5-10 minutes.
    * Go to "Virtual Machines", you should see it there.
      
      ![](https://i.imgur.com/RoOnGOa.png)
      
## SSH into your virtual machine

* Click on **Virtual Machines** and then click on your recently-created VM.

  ![](https://i.imgur.com/bEf8kGG.png)

* Copy the **Public IP address**

  ![](https://i.imgur.com/8ydNm2l.png)

* Open a terminal on your local machine.
* SSH into your VM:
  
  ```bash
  ssh <username>@<ip-address>
  ```

## Install JupyterHub

* Follow the guide at https://the-littlest-jupyterhub.readthedocs.io/en/latest/install/custom.html#install-custom

## (optional) Delete your virtual machine

* Go to "Virtual Machines"
* Click your machine name
* Click on "Stop" to stop the machine temporarily, or "Delete" to delete it permanently.

![](https://i.imgur.com/6CgoYDx.png)
