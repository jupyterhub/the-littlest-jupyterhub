.. _howto/env/user_environment:

==================================
Install conda, pip or apt packages
==================================

:abbr:`TLJH (The Littlest JupyterHub)` starts all users in the same `conda <https://conda.io/docs/>`_
environment. Packages / libraries installed in this environment are available
to all users on the JupyterHub. Users with :ref:`admin rights <howto/admin/admin-users>` can install packages
easily.

.. _howto/env/user_environment_pip:

Installing pip packages
=======================

`pip <https://pypi.org/project/pip/>`_ is the recommended tool for installing packages
in Python from the `Python Packaging Index (PyPI) <https://pypi.org/>`_. PyPI has
almost 145,000 packages in it right now, so a lot of what you need is going to be there!

1. Log in as an admin user and open a Terminal in your Jupyter Notebook.

   .. image:: ../../images/notebook/new-terminal-button.png
      :alt: New Terminal button under New menu

   If you already have a terminal open as an admin user, that should work too!

2. Install a package!

   .. code-block:: bash

      sudo -E pip install numpy

   This installs the ``numpy`` library from PyPI and makes it available
   to all users.

   .. note::

      If you get an error message like ``sudo: pip: command not found``,
      make sure you are not missing the ``-E`` parameter after ``sudo``.

.. _howto/env/user_environment_conda:

Installing conda packages
=========================

Conda lets you install new languages (such as new versions of python, node, R, etc)
as well as packages in those languages. For lots of scientific software, installing
with conda is often simpler & easier than installing with pip - especially if it
links to C / Fortran code.

We recommend installing packages from `conda-forge <https://conda-forge.org/>`_,
a community maintained repository of  conda packages.

1. Log in as an admin user and open a Terminal in your Jupyter Notebook.

   .. image:: ../../images/notebook/new-terminal-button.png
      :alt: New Terminal button under New menu

   If you already have a terminal open as an admin user, that should work too!

2. Install a package!

   .. code-block:: bash

      sudo -E conda install -c conda-forge gdal

   This installs the ``gdal`` library from ``conda-forge`` and makes it available
   to all users. ``gdal`` is much harder to install with pip.

   .. note::

      If you get an error message like ``sudo: conda: command not found``,
      make sure you are not missing the ``-E`` parameter after ``sudo``.

.. _howto/env/user_environment_apt:

Installing apt packages
=======================

`apt <https://help.ubuntu.com/lts/serverguide/apt.html.en>`_ is the official package
manager for the `Ubuntu Linux distribution <https://www.ubuntu.com/>`_. You can install
utilities (such as ``vim``, ``sl``, ``htop``, etc), servers (``postgres``, ``mysql``, ``nginx``, etc)
and a lot more languages than present in ``conda`` (``haskell``, ``prolog``, ``INTERCAL``).
Some third party software (such as `RStudio <https://www.rstudio.com/products/rstudio/download/>`_)
is distributed as ``.deb`` files, which are the files ``apt`` uses to install software.

You can search for packages with `Ubuntu Package search <https://packages.ubuntu.com/>`_ -
make sure to look in the version of Ubuntu you are using!

1. Log in as an admin user and open a Terminal in your Jupyter Notebook.

   .. image:: ../../images/notebook/new-terminal-button.png
      :alt: New Terminal button under New menu

   If you already have a terminal open as an admin user, that should work too!

2. Update list of packages available. This makes sure you get the latest version of
   the packages possible from the repositories.

   .. code-block:: bash

      sudo apt update

3. Install the packages you want.

   .. code-block:: bash

      sudo apt install mysql-server git

   This installs (and starts) a ``MySQL <https://www.mysql.com/>`` database server
   and ``git``.


User environment location
=========================

The user environment is a conda environment set up in ``/opt/tljh/user``, with
a Python3 kernel as the default. It is readable by all users, but writeable only
by users who have root access. This makes it possible for JupyterHub admins (who have
root access with ``sudo``) to install software in the user environment easily.

Accessing user environment outside JupyterHub
=============================================

We add ``/opt/tljh/user/bin`` to the ``$PATH`` environment variable for all JupyterHub
users, so everything installed in the user environment is available to them automatically.
If you are using ``ssh`` to access your server instead, you can get access to the same
environment with:

.. code-block:: bash

   export PATH=/opt/tljh/user/bin:${PATH}

Whenever you run any command now, the user environment will be searched first before
your system environment is. So if you run ``python3 <somefile>``, it'll use the ``python3``
installed in the user environment (``/opt/tljh/user/bin/python3``) rather than the ``python3``
installed in your system environment (``/usr/bin/python3``). This is usually what you want!

To make this change 'stick', you can add the line to the end of the ``.bashrc`` file in
your home directory.

When using ``sudo``, the ``PATH`` environment variable is usually reset, for security
reasons. This leads to error messages like:

.. code-block:: console

   $ sudo conda install -c conda-forge gdal
   sudo: conda: command not found

The most common & portable way to fix this when using ``ssh`` is:

.. code-block:: bash

   sudo PATH=${PATH} conda install -c conda-forge gdal


Upgrade to a newer Python version
=================================

All new TLJH installs use miniconda 4.7.10, which comes with a Python 3.7
environment for the users. The previously TLJH installs came with miniconda 4.5.4,
which meant a Python 3.6 environment.

To upgrade the Python version of the user environment, one can:

*  **Start fresh on a machine that doesn't have TLJH already installed.**

   See the :ref:`installation guide <install/installing>` section about how to install TLJH.

*  **Upgrade Python manually.**

   Because upgrading Python for existing installs can break packages alaredy installed
   under the old Python, upgrading your current TLJH installation, will NOT upgrade
   the Python version of the user environment, but you may do so manually.

   **Steps:**

   1. Activate the user environment, if using ssh.
      If the terminal was started with JupyterHub, this step can be skipped:

      .. code-block:: bash

         source /opt/tljh/user/bin/activate

   2. Get the list of currently installed pip packages (so you can later install them under the
      new Python):

      .. code-block:: bash

         pip freeze > pip_pkgs.txt

   3. Update all conda installed packages in the environment:

      .. code-block:: bash

         sudo PATH=${PATH} conda update --all

   4. Update Python version:

      .. code-block:: bash

         sudo PATH=${PATH} conda install python=3.7

   5. Install the pip packages previously saved:

      .. code-block:: bash

         pip install -r pip_pkgs.txt
