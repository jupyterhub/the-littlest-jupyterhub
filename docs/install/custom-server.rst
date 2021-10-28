.. _install/custom:

=============================
Installing on your own server
=============================


Follow this guide if your cloud provider doesn't have a direct tutorial, or
you are setting this up on a bare metal server.

.. warning::

   Do **not** install TLJH directly on your laptop or personal computer!
   It will most likely open up exploitable security holes when run directly
   on your personal computer.

.. note::

   Running TLJH *inside* a docker container is not supported, since we depend
   on systemd. If you want to run TLJH locally for development, see
   :ref:`contributing/dev-setup`.

Goal
====

By the end of this tutorial, you should have a JupyterHub with some admin
users and a user environment with packages you want installed running on
a server you have access to.

Pre-requisites
==============

#. Some familiarity with the command line.
#. A server running Ubuntu 18.04 where you have root access.
#. At least **1GB** of RAM on your server.
#. Ability to ``ssh`` into the server & run commands from the prompt.
#. An **IP address** where the server can be reached from the browsers of your target audience.

If you run into issues, look at the specific :ref:`troubleshooting guide <troubleshooting/providers/custom>`
for custom server installations.

Step 1: Installing The Littlest JupyterHub
==========================================

#. Using a terminal program, SSH into your server. This should give you a prompt where you can
   type commands.

#. Make sure you have ``python3``, ``python3-dev``, ``curl`` and ``git`` installed.

   .. code::

      sudo apt install python3 python3-dev git curl

#. Copy the text below, and paste it into the terminal. Replace
   ``<admin-user-name>`` with the name of the first **admin user** for this
   JupyterHub. Choose any name you like (don't forget to remove the brackets!).
   This admin user can log in after the JupyterHub is set up, and
   can configure it to their needs. **Remember to add your username**!

   .. code-block:: bash

      curl -L https://tljh.jupyter.org/bootstrap.py | sudo -E python3 - --admin <admin-user-name>

   .. note::

      See :ref:`topic/installer-actions` if you want to understand exactly what the installer is doing.
      :ref:`topic/customizing-installer` documents other options that can be passed to the installer.

#. Press ``Enter`` to start the installation process. This will take 5-10 minutes,
   and will say ``Done!`` when the installation process is complete.

#. Copy the **Public IP** of your server, and try accessing ``http://<public-ip>`` from
   your browser. If everything went well, this should give you a JupyterHub login page.

   .. image:: ../images/first-login.png
      :alt: JupyterHub log-in page

#. Login using the **admin user name** you used in step 3. You can choose any
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
