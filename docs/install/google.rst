.. _install/google:

==========================
Installing on Google Cloud
==========================

Goal
====

By the end of this tutorial, you should have a JupyterHub with some admin
users and a user environment with packages you want installed running on
`Google Cloud <https://cloud.google.com/>`_.

Prerequisites
=============

#. A Google Cloud account. You might use the free credits for trying it out!

Step 1: Installing The Littlest JupyterHub
==========================================

Let's create the server on which we can run JupyterHub.

#. Log in to `Google Cloud Console <https://console.cloud.google.com>`_ with
   your Google Account.

#. Open the navigation menu by clicking the button with three lines on the top
   left corner of the page.

   .. image:: ../images/providers/google/left-menu-button.png
      :alt: Button to open the menu

   This opens a menu with all the cloud products Google Cloud offers.

#. Under **Compute Engine**, select **VM Instances**.

   .. image:: ../images/providers/google/vm-instances-menu.png
      :alt: Navigation Menu -> Compute Engine -> VM Instances

#. If you are using Google Cloud for the first time, you might have to
   enable billing. Google will present a screen asking you to enable billing
   to proceed. Click the **Enable Billing** button and follow any prompts
   that appear.

   .. image:: ../images/providers/google/enable-billing.png
      :alt: Enable billing if needed.

   It might take a few minutes for your account to be set up.

#. Once Compute Engine is ready, click the **Create** button to start
   creating the server that'll run TLJH.

   .. image:: ../images/providers/google/create-vm-first.png
      :alt: Create VM page when using it for the first time.

   If you already have VMs running in your project, the screen will look
   different. But you can find the **Create** button still!

#. This shows you a page titled **Create an instance**. This lets you customize
   the kind of server you want, the resources it will have & what it'll be called.

#. Under **Name**, give it a memorable name that identifies what purpose this
   JupyterHub will be used for.

#. **Region** specifies the physical location where this server will be hosted.
   Generally, pick something close to where most of your users are. Note that
   it might increase the cost of your server in some cases!

#. For **Zone**, pick any of the options. Leaving the default as is is fine.

#. Under **Machine** type, select the amount of CPU / RAM / GPU you want for your
   server. You need at least **1GB** of RAM.

   You can select a preset combination in the default **basic view**.

   .. image:: ../images/providers/google/machine-type-basic.png
      :alt: Select a preset VM type

   If you want to add **GPUs**, you should click the **Customize** button &
   use the **Advanced View**. You need to request `a quota increase <https://cloud.google.com/compute/quotas#gpus>`_
   before you can use GPUs.

   .. image:: ../images/providers/google/machine-type-advanced.png
      :alt: Select a customized VM size

   Check out our guide on How To :ref:`howto/admin/resource-estimation` to help pick
   how much Memory / CPU your server needs.

#. Under **Boot Disk**, click the **Change** button. This lets us change the
   operating system and the size of your disk.

   .. image:: ../images/providers/google/boot-disk-button.png
      :alt: Changing Boot Disk & disk size

   This should open a **Boot disk** popup.

#. Select **Ubuntu 18.04 LTS** from the list of operating system images.

   .. image:: ../images/providers/google/boot-disk-ubuntu.png
      :alt: Selecting Ubuntu 18.04 for OS

#. You can also change the **type** and **size** of your disk at the bottom
   of this popup.

   .. image:: ../images/providers/google/boot-disk-size.png
      :alt: Selecting Boot disk type & size

   **Standard persistent disk** type gives you a slower but cheaper disk, similar
   to a hard drive. **SSD persistent disk** gives you a faster but more expensive
   disk, similar to an SSD.

   Check out our guide on How To :ref:`howto/admin/resource-estimation` to help pick
   how much Disk space your server needs.

#. Click the **Select** button to dismiss the Boot disk popup and go back to the
   Create an instance screen.

#. Under **Identity and API access**, select **No service account** for the
   **Service account** field. This prevents your JupyterHub users from automatically
   accessing other cloud services, increasing security.

   .. image:: ../images/providers/google/no-service-account.png
      :alt: Disable service accounts for the server

#. Under **Firewall**, check both **Allow HTTP Traffic** and **Allow HTTPS Traffic**
   checkboxes.

   .. image:: ../images/providers/google/firewall.png
      :alt: Allow HTTP & HTTPS traffic to your server

#. Click the **Management, disks, networking, SSH keys** link to expand more
   options.

   .. image:: ../images/providers/google/management-button.png
      :alt: Expand management options by clicking link.

   This displays a lot of advanced options, but we'll be only using one of them.

#. Copy the text below, and paste it into the **Startup script** text box. Replace
   ``<admin-user-name>`` with the name of the first **admin user** for this
   JupyterHub. This admin user can log in after the JupyterHub is set up, and
   can configure it to their needs. **Remember to add your username**!

   .. code-block:: bash

       #!/bin/bash
       curl -L https://tljh.jupyter.org/bootstrap.py \
         | sudo python3 - \
           --admin <admin-user-name>

   .. image:: ../images/providers/google/startup-script.png
      :alt: Install JupyterHub with the Startup script textbox

   .. note::

      See :ref:`topic/installer-actions` if you want to understand exactly what the installer is doing.
      :ref:`topic/customizing-installer` documents other options that can be passed to the installer.

#. Click the **Create** button at the bottom to start your server!

   .. image:: ../images/providers/google/create-vm-button.png
      :alt: Launch an Instance / Advanced Options dialog box

#. We'll be sent to the **VM instances** page, where we can see that our server
   is being created.

   .. image:: ../images/providers/google/vm-creating.png
      :alt: Spinner with vm creating

#. In a few seconds your server will be created, and you can see the **External IP**
   used to access it.

   .. image:: ../images/providers/google/vm-created.png
      :alt: VM created, external IP available

#. The Littlest JupyterHub is now installing in the background on your new server.
   It takes around 5-10 minutes for this installation to complete.

#. Check if the installation is complete by **copying** the **External IP**
   of your server, and trying to access it with a browser. Do **not click** on the
   IP - this will open the link with HTTPS, and will not work.

   Accessing the JupyterHub will also fail until the installation is complete,
   so be patient.

#. When the installation is complete, it should give you a JupyterHub login page.

   .. image:: ../images/first-login.png
      :alt: JupyterHub log-in page

#. Login using the **admin user name** you used in step 6, and a password. Use a
   strong password & note it down somewhere, since this will be the password for
   the admin user account from now on.

#. Congratulations, you have a running working JupyterHub!

Step 2: Adding more users
==========================

.. include:: add_users.txt

Step 3: Install conda / pip packages for all users
==================================================

.. include:: add_packages.txt
