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

The Littlest JupyterHub (TLJH) can run on any server that is running at least
**Ubuntu 18.04**. Earlier versions of Ubuntu are not supported.
We have a bunch of tutorials to get you started.

- Tutorials to create a new server from scratch on a cloud provider & run TLJH
  on it. These are **recommended** if you do not have much experience setting up
  servers.

  .. toctree::
     :titlesonly:
     :caption: Installation

     install/digitalocean
     install/jetstream
     install/google
     install/amazon
     install/custom-server

Once you are ready to run your server for real,
it's a good idea to proceed directly to :doc:`howto/admin/https`.

How-To Guides
=============

How-To guides answer the question 'How do I...?' for a lot of topics.

Content and Data
----------------

.. toctree::
   :titlesonly:
   :caption: Content and data

   howto/content/nbgitpuller
   howto/content/add-data
   howto/content/share-data

The user environment
--------------------

.. toctree::
   :titlesonly:
   :caption: The user environment

   howto/env/user-environment
   howto/env/notebook-interfaces
   howto/env/server-resources

Authentication
--------------

We have a special set of How-To Guides on using various forms of authentication
with your JupyterHub. For more information on Authentication, see
:ref:`topic/authenticator-configuration`

.. toctree::
   :titlesonly:
   :caption: Authentication

   howto/auth/dummy
   howto/auth/github
   howto/auth/firstuse
   howto/auth/nativeauth

Administration and security
---------------------------

.. toctree::
   :titlesonly:
   :caption: Administration and security

   howto/admin/admin-users
   howto/admin/resource-estimation
   howto/admin/resize
   howto/admin/nbresuse
   howto/admin/https
   howto/admin/enable-extensions

Cloud provider configuration
----------------------------

.. toctree::
   :titlesonly:
   :caption: Cloud provider configuration

   howto/providers/digitalocean

Topic Guides
============

Topic guides provide in-depth explanations of specific topics.

.. toctree::
   :titlesonly:
   :caption: Topic guides

   topic/whentouse
   topic/requirements
   topic/security
   topic/customizing-installer
   topic/installer-actions
   topic/tljh-config
   topic/authenticator-configuration
   topic/escape-hatch


Troubleshooting
===============

In time, all systems have issues that need to be debugged. Troubleshooting
guides help you find what is broken & hopefully fix it.

.. toctree::
   :titlesonly:
   :caption: Troubleshooting

   troubleshooting/logs

Often, your issues are not related to TLJH itself but to the cloud provider
your server is running on. We have some documentation on common issues you
might run into with various providers and how to fix them. We welcome contributions
here to better support your favorite provider!

.. toctree::
   :titlesonly:

   troubleshooting/providers/google
   troubleshooting/providers/amazon
   troubleshooting/providers/custom

Contributing
============

We want you to contribute to TLJH in the ways that are most useful
and exciting to you. This section contains documentation helpful
to people contributing in various ways.

.. toctree::
   :titlesonly:
   :caption: Contributing

   contributing/docs
   contributing/code-review
   contributing/dev-setup
   contributing/tests
   contributing/plugins
   contributing/packages
