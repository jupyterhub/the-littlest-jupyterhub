.. _tutorial_quickstart_digitalocean:

Tutorial: JupyterHub on Digital Ocean
========================================

Goal
----

By the end of this tutorial, you should have a JupyterHub with some admin
users and a user environment with packages you want installed running on
`DigitalOcean <https://digitalocean.com>`_.

Pre-requisites
--------------

#. A DigitalOcean account with a payment method attached.
#. Some familiarity with the command line.

Step 1: Installing The Littlest JupyterHub
------------------------------------------

Let's create the server on which we can run JupyterHub.

#. Log in to `DigitalOcean <https://digitalocean.com>`_. You might need to
   attach a credit card or other payment method to your account before you
   can proceed with the tutorial.

#. Click the **Create** button on the top right, and select **Droplets** from
   the dropdown menu. DigitalOcean calls servers **droplets**.

   .. image:: images/digitalocean/create-menu.png
      :alt: Dropdown menu on clicking 'create' in top right corner

   This takes you to a page titled **Create Droplets** that lets you configure
   your server.

#. Under **Choose an image**, select **18.04 x64** under **Ubuntu**.

   .. image:: images/digitalocean/select-image.png
      :alt: Select 18.04 x64 image under Ubuntu

#. Under **Choose a size**, select the size of the server you want. The default
   (4GB RAM, 2CPUs, 20 USD / month) is not a bad start. You can resize your server
   later if you need.

#. Scroll down to **Select additional options**, and select **User data**.

   .. image:: images/digitalocean/additional-options.png
      :alt: Turn on User Data in additional options

   This opens up a textbox where you can enter a script that will be run
   when the server is created. We will use this to set up The Littlest JupyterHub
   on this server.

#. Copy the text below, and paste it into the user data text box. Replace
   ``<admin-user-name>`` with the name of the first **admin user** for this
   JupyterHub. This admin user can log in after the JupyterHub is set up, and
   can configure it to their needs. Remember the username!

   .. code-block:: bash

    #!/bin/bash
    curl https://raw.githubusercontent.com/yuvipanda/the-littlest-jupyterhub/master/bootstrap/bootstrap.py \
     | sudo python3 - \
       --admin <admin-user-name>

#. Under the **Finalize and create** section, enter a ``hostname`` that descriptively
   identifies this server for you.

   .. image:: images/digitalocean/hostname.png
      :alt: Select suitable hostname for your server

#. Click the **Create** button! You will be taken to a different screen,
   where you can see progress of your server being created.

   .. image:: images/digitalocean/server-create-wait.png
      :alt: Server being created

#. In a few seconds your server will be created, and you can see the **public IP**
   used to access it.

   .. image:: images/digitalocean/server-create-done.png
      :alt: Server finished creating, public IP available

#. The Littlest JupyterHub is now installing in the background on your new server.
   It takes around 5-10 minutes for this installation to complete.

#. Check if the installation is complete by copying the **public ip**
   of your server, and trying to access it with a browser. This will fail until
   the installation is complete, so be patient.

#. When the installation is complete, it should give you a JupyterHub login page.

   .. image:: images/first-login.png
      :alt: JupyterHub log-in page

#. Login using the **admin user name** you used in step 6, and a password. Use a
   strong password & note it down somewhere, since this will be the password for
   the admin user account from now on.

#. Congratulations, you have a running working JupyterHub!

Step 2: Addding more users
--------------------------

Most administration & configuration of the JupyterHub can be done from the
web UI directly. Let's add a few users who can log in!

#. Open the **Control Panel** by clicking the control panel button on the top
   right of your JupyterHub.

   .. image:: ../images/control-panel-button.png
      :alt: Control panel button in notebook, top right

#. In the control panel, open the **Admin** link in the top left.

   .. image:: ../images/admin-button.png
      :alt: Admin button in control panel, top left

   This opens up the JupyterHub admin page, where you can add / delete users,
   start / stop peoples' servers and see who is online.

#. Click the **Add Users** button.

   .. image:: ../images/admin/add-users-button.png
      :alt: Add Users button in the admin page

   A **Add Users** dialog box opens up.

#. Type the names of users you want to add to this JupyterHub in the dialog box,
   one per line.

   .. image:: ../images/admin/add-users-dialog.png
      :alt: Adding users with add users dialog

   You can tick the **Admin** checkbox if you want to give admin rights to all
   these users too.

#. Click the **Add Users** button in the dialog box. Your users are now added
   to the JupyterHub! When they log in for the first time, they can set their
   password - and use it to log in again in the future.

Congratulations, you now have a multi user JupyterHub that you can add arbitrary
users to!

Step 3: Install conda / pip packages for all users
--------------------------------------------------

The **User Environment** is a conda environment that is shared by all users
in the JupyterHub. Libraries installed in this environment are immediately
available to all users. Admin users can install packages in this environment
with ``sudo -E``.

#. Log in as an admin user and open a Terminal in your Jupyter Notebook.

   .. image:: ../images/new_terminal_button.png
      :alt: New Terminal button under New menu

#. Install `gdal <https://anaconda.org/conda-forge/gdal>`_ from `conda-forge <https://conda-forge.org/>`_.

   .. code-block:: bash

      sudo -E conda install -c conda-forge gdal

   The ``sudo -E`` is very important!

#. Install ``there`` with ``pip``

   .. code-block:: bash

      sudo -E pip install there

The packages ``gdal`` and ``there`` are now available to all users in JupyterHub.
If a user already had a python notebook running, they have to restart their notebook's
kernel to make the new libraries available.

See :ref:`user_environment` for more information.
