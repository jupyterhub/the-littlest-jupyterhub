.. _insatll/digitalocean:

===========================
Installing on Digital Ocean
===========================

Goal
====

By the end of this tutorial, you should have a JupyterHub with some admin
users and a user environment with packages you want installed running on
`DigitalOcean <https://digitalocean.com>`_.

Pre-requisites
==============

#. A DigitalOcean account with a payment method attached.

Step 1: Installing The Littlest JupyterHub
==========================================

Let's create the server on which we can run JupyterHub.

#. Log in to `DigitalOcean <https://digitalocean.com>`_. You might need to
   attach a credit card or other payment method to your account before you
   can proceed with the tutorial.

#. Click the **Create** button on the top right, and select **Droplets** from
   the dropdown menu. DigitalOcean calls servers **droplets**.

   .. image:: ../images/providers/digitalocean/create-menu.png
      :alt: Dropdown menu on clicking 'create' in top right corner

   This takes you to a page titled **Create Droplets** that lets you configure
   your server.

#. Under **Choose an image**, select **18.04 x64** under **Ubuntu**.

   .. image:: ../images/providers/digitalocean/select-image.png
      :alt: Select 18.04 x64 image under Ubuntu

#. Under **Choose a size**, select the size of the server you want. The default
   (4GB RAM, 2CPUs, 20 USD / month) is not a bad start. You can resize your server
   later if you need.

   Check out our guide on How To :ref:`howto/admin/resource-estimation` to help pick
   how much Memory, CPU & disk space your server needs.

#. Scroll down to **Select additional options**, and select **User data**.

   .. image:: ../images/providers/digitalocean/additional-options.png
      :alt: Turn on User Data in additional options

   This opens up a textbox where you can enter a script that will be run
   when the server is created. We will use this to set up The Littlest JupyterHub
   on this server.

#. Copy the text below, and paste it into the user data text box. Replace
   ``<admin-user-name>`` with the name of the first **admin user** for this
   JupyterHub. This admin user can log in after the JupyterHub is set up, and
   can configure it to their needs. **Remember to add your username**!

   .. code-block:: bash

      #!/bin/bash
      curl -L https://tljh.jupyter.org/bootstrap.py \
        | sudo python3 - \
          --admin <admin-user-name>

   .. note::

      See :ref:`topic/installer-actions` if you want to understand exactly what the installer is doing.
      :ref:`topic/customizing-installer` documents other options that can be passed to the installer.

#. Under the **Finalize and create** section, enter a ``hostname`` that descriptively
   identifies this server for you.

   .. image:: ../images/providers/digitalocean/hostname.png
      :alt: Select suitable hostname for your server

#. Click the **Create** button! You will be taken to a different screen,
   where you can see progress of your server being created.

   .. image:: ../images/providers/digitalocean/server-create-wait.png
      :alt: Server being created

#. In a few seconds your server will be created, and you can see the **public IP**
   used to access it.

   .. image:: ../images/providers/digitalocean/server-create-done.png
      :alt: Server finished creating, public IP available

#. The Littlest JupyterHub is now installing in the background on your new server.
   It takes around 5-10 minutes for this installation to complete.

#. Check if the installation is complete by copying the **public ip**
   of your server, and trying to access it with a browser. This will fail until
   the installation is complete, so be patient.

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
