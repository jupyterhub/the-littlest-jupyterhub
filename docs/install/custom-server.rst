.. _install/custom:

=============================
Installing on your own server
=============================

.. note::

    You should use this if your cloud provider does not already have a direct tutorial,
    or if you have experience setting up servers.


Goal
====

By the end of this tutorial, you should have a JupyterHub with some admin
users and a user environment with packages you want installed running on
a server you have access to.

Pre-requisites
==============

#. Some familiarity with the command line.
#. A server running Ubuntu 18.04 where you have root access.
#. Ability to ``ssh`` into the server & run commands from the prompt.
#. A **IP address** where the server can be reached from the browsers of your target audience.

Step 1: Installing The Littlest JupyterHub
==========================================

#. Using a terminal program, SSH into your server. This should give you a prompt where you can
   type commands.

#. If your server is behind a firewall and needs a proxy:

   .. code-block:: bash

      export http_proxy=<your_proxy>

#. Some requests will fail if your certs are self-signed. Copy the text below and paste it
   into the terminal after replacing ``</directory/with/your/ssl/certificates>`` 
   with the **path of the directory containing your ssl certificates** (don't include the brackets!).:

   .. code::

      export REQUESTS_CA_BUNDLE=</directory/with/your/ssl/certificates>
      sudo npm config set cafile=</directory/with/your/ssl/certificates>

#. Make sure you have ``Python3``, ``curl`` and ``git``  installed. On latest Ubuntu you can get all of these with:

   .. code::

      apt-get install python3 git curl

#. Copy the text below, and paste it into the terminal. Replace
   ``<admin-user-name>`` with the name of the first **admin user** for this
   JupyterHub. Choose any name you like (don't forget to replace the brackets!).
   This admin user can log in after the JupyterHub is set up, and
   can configure it to their needs. **Remember to add your username**!

   .. code-block:: bash

      curl https://raw.githubusercontent.com/jupyterhub/the-littlest-jupyterhub/master/bootstrap/bootstrap.py | sudo -E python3 - --admin <admin-user-name>

   .. note::

      See :ref:`topic/installer-actions` if you want to understand exactly what the installer is doing.
      :ref:`topic/customizing-installer` documents other options that can be passed to the installer.

#. Press ``Enter`` to start the installation process. This will take 5-10 minutes,
   and will say 'Done!' when the installation process is complete.

#. Copy the **Public IP** of your server, and try accessing ``http://<public-ip>`` from
   your browser. If everything went well, this should give you a JupyterHub login page.

   .. image:: ../images/first-login.png
      :alt: JupyterHub log-in page

#. Login using the **admin user name** you used in step 2. You can choose any
   password that you wish. Use a
   strong password & note it down somewhere, since this will be the password for
   the admin user account from now on.

#. Congratulations, you have a running working JupyterHub!

Step 2: Adding more users
==========================

.. include:: add_users.txt

Step 3: Install conda / pip packages for all users
==================================================

.. include:: add_packages.txt

Step 4: Setup HTTPS
===================

Once you are ready to run your server for real, and have a domain, it's a good
idea to proceed directly to :ref:`howto/admin/https`.

