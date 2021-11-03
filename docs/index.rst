=======================
The Littlest JupyterHub
=======================

A simple `JupyterHub <https://github.com/jupyterhub/jupyterhub>`_ distribution for
a small (0-100) number of users on a single server. We recommend reading
:ref:`topic/whentouse` to determine if this is the right tool for you.


Development Status
==================

This project is currently in **beta** state. Folks have been using installations
of TLJH for more than a year now to great success. While we try hard not to, we
might still make breaking changes that have no clear upgrade pathway.

Installation
============

The Littlest JupyterHub (TLJH) can run on any server that is running **Ubuntu 18.04** or **Ubuntu 20.04** on a amd64 or arm64 CPU architecture. Earlier versions of Ubuntu are not supported.
We have a bunch of tutorials to get you started.

- Tutorials to create a new server from scratch on a cloud provider & run TLJH
  on it. These are **recommended** if you do not have much experience setting up
  servers.

  .. toctree::
     :titlesonly:
     :maxdepth: 2

     install/index

Once you are ready to run your server for real,
it's a good idea to proceed directly to :doc:`howto/admin/https`.

How-To Guides
=============

How-To guides answer the question 'How do I...?' for a lot of topics.

.. toctree::
   :maxdepth: 2

   howto/index

Topic Guides
============

Topic guides provide in-depth explanations of specific topics.

.. toctree::
   :titlesonly:
   :maxdepth: 2

   topic/index


Troubleshooting
===============

In time, all systems have issues that need to be debugged. Troubleshooting
guides help you find what is broken & hopefully fix it.

.. toctree::
   :titlesonly:
   :maxdepth: 2

   troubleshooting/index

Contributing
============

We want you to contribute to TLJH in the ways that are most useful
and exciting to you. This section contains documentation helpful
to people contributing in various ways.

.. toctree::
   :titlesonly:
   :maxdepth: 2

   contributing/index
