.. _install/ovh:

=================
Installing on OVH
=================

Goal
====

By the end of this tutorial, you should have a JupyterHub with some admin
users and a user environment with packages you want installed running on
`OVH <https://www.ovh.com>`_.

Pre-requisites
==============

#. An OVH account.

Step 1: Installing The Littlest JupyterHub
==========================================

Let's create the server on which we can run JupyterHub.

#. Log in to the `OVH Control Panel <https://www.ovh.com/auth/>`_.

#. Click the **Public Cloud** button in the navigation bar.

   .. image:: ../images/providers/ovh/public-cloud.png
      :alt: Public Cloud entry in the navigation bar

#. If you don't have an OVH Stack, you can create one by clicking on the following button:

   .. image:: ../images/providers/ovh/create-ovh-stack.png
      :alt: Button to create an OVH stack
      
#. Select a name for the project:

   .. image:: ../images/providers/ovh/project-name.png
      :alt: Select a name for the project

#. If you don't have a payment method yet, select one and click on "Create my project":

   .. image:: ../images/providers/ovh/payment.png
      :alt: Select a payment method

#. Using the **Public Cloud interface**, click on **Create an instance**:

   .. image:: ../images/providers/ovh/create-instance.png
      :alt: Create a new instance
      
#. **Select a model** for the instance. A good start is the **S1-4** model under **Shared resources** which comes with 4GB RAM, 1 vCores and 20GB SSD.
      
#. **Select a region**.

#. Select **Ubuntu 18.04** as the image:

   .. image:: ../images/providers/ovh/distribution.png
      :alt: Select Ubuntu 18.04 as the image

#. OVH requires setting an SSH key to be able to connect to the instance.
   You can create a new SSH by following
   `these instructions <https://help.github.com/en/enterprise/2.16/user/articles/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent>`_.
   Be sure to copy the content of the ``~/.ssh/id_rsa.pub`` file, which corresponds to the **public part** of the SSH key.

#. Select **Configure your instance**, and select a name for the instance.
   Under **Post-installation script**, copy the text below and paste it in the text box.
   Replace ``<admin-user-name>`` with the name of the first **admin user** for this
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


   .. image:: ../images/providers/ovh/configuration.png
      :alt: Add post-installation script

#. Select a billing period: monthly or hourly.

#. Click the **Create an instance** button! You will be taken to a different screen,
   where you can see progress of your server being created.

   .. image:: ../images/providers/ovh/create-instance.png
      :alt: Select suitable hostname for your server

#. In a few seconds your server will be created, and you can see the **public IP**
   used to access it.

   .. image:: ../images/providers/ovh/public-ip.png
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
