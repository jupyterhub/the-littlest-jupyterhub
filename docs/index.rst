=======================
The Littlest JupyterHub
=======================

A simple `JupyterHub <https://github.com/jupyterhub/jupyterhub>`_ distribution for
a small (0-100) number of users on a single server. We recommend reading
:ref:`topic/whentouse` to determine if this is the right tool for you.

Development Status
==================

This project is currently in **alpha** state. Most things work, but we might
still make breaking changes that have no clear upgrade pathway. We are targeting
a v0.1 release sometime in mid-August 2018. Follow `this milestone <https://github.com/jupyterhub/the-littlest-jupyterhub/milestone/1>`_
to see progress towards the release!

Installation
============

The Littlest JupyterHub (TLJH) can run on any server that is running at least
Ubuntu 18.04. We have a bunch of tutorials to get you started.

- Tutorials to create a new server from scratch on a cloud provider & run TLJH
  on it. These are **recommended** if you do not have much experience setting up
  servers.

  .. toctree::
     :titlesonly:

     install/digitalocean
     install/jetstream
     install/google

- :ref:`install/custom`.
  You should use this if your cloud provider does not already have a direct tutorial,
  or if you have experience setting up servers.

Once you are ready to run your server for real,
it's a good idea to proceed directly to :doc:`howto/https`.

Tutorials
=========

Tutorials guide you step-by-step through accomplishing a specific task.

.. toctree::
   :titlesonly:

   tutorials/nbgitpuller.rst

How-To Guides
=============

How-To guides answer the question 'How do I...?' for a lot of topics.

.. toctree::
   :titlesonly:

   howto/https
   howto/user-environment
   howto/admin-users
   howto/share-data
   howto/notebook-interfaces
   howto/resource-estimation
   howto/nbresuse

Authentication
--------------

We have a special set of How-To Guides on using various forms of authentication
with your JupyterHub. For more information on Authentication, see
:ref:`topic/authenticator-configuration`

.. toctree::
   :titlesonly:

   howto/auth/dummy
   howto/auth/github

Topic Guides
============

Topic guides provide in-depth explanations of specific topics.

.. toctree::
   :titlesonly:

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

   troubleshooting/logs

Often, your issues are not related to TLJH itself but to the cloud provider
your server is running on. We have some documentation on common issues you
might run into with various providers and how to fix them. We welcome contributions
here to better support your favorite provider!

.. toctree::
   :titlesonly:

   troubleshooting/providers/google

Contributing
============

We want you to contribute to TLJH in the ways that are most useful
and exciting to you. This section contains documentation helpful
to people contributing in various ways.

.. toctree::
   :titlesonly:

   contributing/docs
   contributing/code-review
   contributing/dev-setup
