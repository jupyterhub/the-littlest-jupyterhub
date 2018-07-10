.. _installation:

============
Installation
============

Quick Installation
==================

The quick way to install The Littlest JupyterHub (tljh) is:

.. code-block:: bash

   curl https://raw.githubusercontent.com/yuvipanda/the-littlest-jupyterhub/master/bootstrap/bootstrap.py | sudo python3 -

This takes 2-5 minutes to run. When completed, you can access your new JupyterHub
at the public IP of your server!

You should probably add yourself as an `admin user <admin.rst>`_
after installation.

Slightly less quick installation
================================

If you can read ``python3`` and are nervous about the previous installation method,
you can inspect the installer script before running it.


1. Download the installer script

   .. code-block:: bash

      curl https://raw.githubusercontent.com/yuvipanda/the-littlest-jupyterhub/master/bootstrap/bootstrap.py -o bootstrap.py

2. Read the install script source using your favorite text editor

3. Run the installer script

   .. code-block:: bash

      sudo python3 bootstrap.py

   This should have the exact same effects as the quick installer method.
