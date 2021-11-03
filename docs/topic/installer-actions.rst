.. _topic/installer-actions:

===========================
What does the installer do?
===========================

This document details what exactly the installer does to the machine it is
run on.

``apt`` Packages installed
==========================

The packages ``python3`` and ``python3-venv`` are installed from the apt repositories.

Hub environment
===============

JupyterHub is run from a python3 virtual environment located in ``/opt/tljh/hub``. It
uses the system's installed python and is owned by root. It also contains a binary install
of `traefik <http://traefik.io/>`_. This virtual environment is completely managed by TLJH.

.. note::
	If you try to remove TLJH, revert this action using:

	.. code-block:: bash

		sudo rm -rf /opt/tljh/hub


User environment
================

By default, a ``mambaforge`` conda environment is installed in ``/opt/tljh/user``. This contains
the notebook interface used to launch all users, and the various packages available to all
users. The environment is owned by the ``root`` user. JupyterHub admins may use
to ``sudo -E conda install`` or ``sudo -E pip install`` packages into this environment.

This conda environment is added to ``$PATH`` for all users started with JupyterHub. If you
are using ``ssh`` instead, you can activate this environment by running the following:

.. code-block:: bash

   source /opt/tljh/user/bin/activate

This should let you run various ``conda`` and ``pip`` commands. If  you run into errors like
``Command 'conda' not found``, try prefixing your command with:

.. code-block:: bash

   sudo env PATH=${PATH} <command>

By default, ``sudo`` does not respect any custom environments you have activated. The ``env PATH=${PATH}``
'fixes' that.

.. note::
	If you try to remove TLJH, revert this action using:

	.. code-block:: bash

		sudo rm -rf /opt/tljh/user

``tljh-config`` symlink
========================

We create a symlink from ``/usr/bin/tljh-config`` to ``/opt/tljh/hub/bin/tljh-config``, so users
can run ``sudo tljh-config <something>`` from their terminal. While the user environment is added
to users' ``$PATH`` when they launch through JupyterHub, the hub environment is not. This makes it
hard to access the ``tljh-config`` command used to change most config parameters. Hence we symlink the
``tljh-config`` command to ``/usr/bin``, so it is directly accessible with ``sudo tljh-config <command>``.

.. note::
	If you try to remove TLJH, revert this action using:

	.. code-block:: bash

		sudo unlink /usr/bin/tljh-config

``jupyterhub_config.d`` directory for custom configuration snippets
===================================================================

Any files in /opt/tljh/config/jupyterhub_config.d that end in .py and are a valid
JupyterHub configuration will be loaded after any of the config options specified
with tljh-config are loaded.

.. note::
	If you try to remove TLJH, revert this action using:

	.. code-block:: bash

		sudo rm -rf /opt/tljh/config

Systemd Units
=============

TLJH places 2 systemd units on your computer. They all start on system startup.

#. ``jupyterhub.service`` - starts the JupyterHub service.
#. ``traefik.service`` - starts traefik proxy that manages HTTPS

In addition, each running Jupyter user gets their own systemd unit of the name ``jupyter-<username>``.

.. note::
	If you try to remove TLJH, revert this action using:

	.. code-block:: bash

		# stop the services
		systemctl stop jupyterhub.service
		systemctl stop traefik.service
		systemctl stop jupyter-<username>

		# disable the services
		systemctl disable jupyterhub.service
		systemctl disable traefik.service
		# run this command for all the Jupyter users
		systemctl disable jupyter-<username>

		# remove the systemd unit
		rm /etc/systemd/system/jupyterhub.service
		rm /etc/systemd/system/traefik.service

		# reset the state of all units
		systemctl daemon-reload
		systemctl reset-failed

State files
===========

TLJH places 3 `jupyterhub.service` and 4 `traefik.service` state files in `/opt/tljh/state`.
These files save the state of JupyterHub and Traefik services and are meant
to be used and modified solely by these services.

.. note::
	If you try to remove TLJH, revert this action using:

	.. code-block:: bash

		sudo rm -rf /opt/tljh/state

Progress page files
===================

If you ran the TLJH installer with the `--show-progress-page` flag, then two files have been
added to your system to help serving the progress page:

* ``/var/run/index.html`` - the main progress page
* ``/var/run/favicon.ico`` - the JupyterHub icon

.. note::
	If you try to remove TLJH, revert this action using:

	.. code-block:: bash

		sudo rm /var/run/index.html
		sudo rm /var/run/favicon.ico


User groups
===========

TLJH creates two user groups when installed:

#. ``jupyterhub-users`` contains all users managed by this JupyterHub
#. ``jupyterhub-admins`` contains all users with admin rights managed by this JupyterHub.

When a new JupyterHub user logs in, a unix user is created for them. The unix user is always added
to the ``jupyterhub-users`` group. If the user is an admin, they are added to the ``jupyterhub-admins``
group whenever they start / stop their notebook server.

If you uninstall TLJH, you should probably remove all user accounts associated with both these
user groups, and then remove the groups themselves. You might have to archive or delete the home
directories of these users under ``/home/``.

.. note::
	If you try to remove TLJH, in order to remove a user and its home directory, use:

	.. code-block:: bash

		sudo userdel -r <user>

Keep in mind that the files located in other parts of the file system
will have to be searched for and deleted manually.

.. note::
	To remove the user groups units:

	.. code-block:: bash

		sudo delgroup jupyterhub-users
		sudo delgroup jupyterhub-admins
		# remove jupyterhub-admins from the sudoers group
		sudo rm /etc/sudoers.d/jupyterhub-admins

Passwordless ``sudo`` for JupyterHub admins
============================================

``/etc/sudoers.d/jupyterhub-admins`` is created to provide passwordless sudo for all JupyterHub
admins. We also set it up to inherit ``$PATH`` with ``sudo -E``, to more easily call ``conda``,
``pip``, etc.


Removing TLJH
=============

If trying to wipe out a fresh TLJH installation, follow the instructions on how to revert
each specific modification the TLJH installer does to the system.

.. note::
	If using a VM, the recommended way to remove TLJH is destroying the VM and start fresh.

.. warning::
	Completely uninstalling TLJH after it has been used is a difficult task because it's
	highly coupled to how the system changed after it has been used and modified by the users.
	Thus, we cannot provide instructions on how to proceed in this case.
