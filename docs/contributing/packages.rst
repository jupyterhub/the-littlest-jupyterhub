.. _contributing/packages:

=======================
Environments & Packages
=======================

TLJH installs packages from different sources during installation.
This document describes the various sources and how to upgrade
versions of packages installed.

Python Environments
===================

TLJH sets up two python environments during installation.

1. **Hub Environment**. JupyterHub, authenticators, spawners, TLJH plugins
   and the TLJH configuration management code is installed into this
   environment. A `venv <https://docs.python.org/3/library/venv.html>`_ is used,
   primarily since conda does not support ARM CPUs and we'd like to support the
   RaspberryPI someday. Admins generally do not install custom packages
   in this environment.

2. **User Environment**. Jupyter Notebook, JupyterLab, nteract, kernels,
   and packages the users wanna use (such as numpy, scipy, etc) are installed
   here. A `conda <https://conda.io>`_ environment is used here, since
   a lot of scientific packages are available from Conda. ``pip`` is still
   used to install Jupyter specific packages, primarily because most notebook
   extensions are still available only on `PyPI <https://pypi.org>`_.
   Admins can install packages here for use by all users.

Python package versions
=======================

In ``installer.py``, most Python packages have a version specified. This
can be upgraded freely whenever needed. Some of them have version checks
in ``integration-tests/test_extensions.py``, so those might need
updating too.

Apt packages
============

Base operating system packages, including Python itself, are installed
via ``apt`` from the base Ubuntu repositories.

We generally do not pin versions of packages provided by apt, instead
just using the latest versions provided by Ubuntu.
