=======================
The Littlest JupyterHub
=======================

A simple `JupyterHub <https://github.com/jupyterhub/jupyterhub>`_ distribution for
a small (0-50) number of users on a single server.

Development Status
==================

This project is currently in **pre-alpha**, and things will break all the time.
There is no supported upgrade pathway, and security issues most likely exist.
However, feedback at this time is extremely valuble, so you should still try
it out!

Installation
============

The Littlest JupyterHub (TLJH) can run on any server that is running at least
Ubuntu 18.04. We have a bunch of tutorials to get you started.

- Tutorials to create a new server from scratch on a cloud provider & run TLJH
  on it. These are **recommended** if you do not have much experience setting up
  servers.

  .. toctree::
     :titlesonly:

     tutorials/digitalocean
     tutorials/jetstream
     tutorials/google

- :ref:`tutorials/custom`.
  You should use this if your cloud provider does not already have a direct tutorial,
  or if you have experience setting up servers.

How-To Guides
=============

How-To guides answer the question 'How do I...?' for a lot of topics.

.. toctree::
   :titlesonly:

   howto/user-environment
   howto/notebook-interfaces
   howto/resource-estimation

Topic Guides
============

Topic guides provide in-depth explanations of specific topics.

.. toctree::
   :titlesonly:

   topic/requirements
   guides/admin
   topic/security
   topic/customizing-installer


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
   contributing/dev-setup
