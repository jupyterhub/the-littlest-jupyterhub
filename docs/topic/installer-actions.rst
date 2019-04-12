.. _topic/installer-actions:

===========================
What does the installer do?
===========================

This document details what exactly the installer does to the machine it is 
run on.

``apt`` Packages installed
==========================

The packages ``python3`` and ``python3-venv`` are installed from the apt repositories.
Since we need an recent & supported version of ``nodejs``, we install it from 
`nodesource <https://github.com/nodesource/distributions>`_.

Hub environment
===============

JupyterHub is run from a python3 virtual environment located in ``/opt/tljh/hub``. It
uses the system's installed python and is owned by root. It also contains a ``npm``
install of `configurable-http-proxy <https://github.com/jupyterhub/configurable-http-proxy>`_
and a binary install of `traefik <http://traefik.io/>`_. This virtual environment is
completely managed by TLJH.

User environment
================

By default, a ``miniconda`` environment is installed in ``/opt/tljh/user``. This contains
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

   sudo PATH=${PATH} <command> 

By default, ``sudo`` does not respect any custom environments you have activated. The ``PATH=${PATH}``
'fixes' that.

``tljh-config`` symlink
========================

We create a symlink from ``/usr/bin/tljh-config`` to ``/opt/tljh/hub/bin/tljh-cohnfig``, so users
can run ``sudo tljh-config <something>`` from their terminal. While the user environment is added
to users' ``$PATH`` when they launch through JupyterHub, the hub environment is not. This makes it
hard to access the ``tljh-config`` command used to change most config parameters. Hence we symlink the
``tljh-config`` command to ``/usr/local/bin``, so it is directly accessible with ``sudo tljh-config <command>``.

Systemd Units
=============

TLJH places 3 systemd units on your computer. They all start on system startup.

#. ``jupyterhub.service`` - starts the JupyterHub service.
#. ``configurable-http-proxy.service`` - starts the nodejs based proxy that is used by JupyterHub.
#. ``traefik.service`` - starts traefik proxy that manages HTTPS

In addition, each running Jupyter user gets their own systemd unit of the name ``jupyter-<username>``.

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

Passwordless ``sudo`` for JupyterHub admins
============================================

``/etc/sudoers.d/jupyterhub-admins`` is created to provide passwordless sudo for all JupyterHub
admins. We also set it up to inherit ``$PATH`` with ``sudo -E``, to more easily call ``conda``,
``pip``, etc.
