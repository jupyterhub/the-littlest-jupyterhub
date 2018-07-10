.. _requirements:

===================
Server Requirements
===================

Operating System
================

We recommend using Ubuntu 18.04 as the base operating system for your server.
Ubuntu 16.04 should also work, but is not officially supported. other Linux
distributions and operating systems are also not officially supported.

Root access
===========

Full ``root`` access to this server is required. This might be via ``sudo``
(recommended) or by direct access to ``root`` (not recommended!)

External IP
===========

An external IP allows users on the internet to reach your JupyterHub. Most
VPS / Cloud providers give you a public IP address along with your server. If
you are hosting on a physical machine somewhere, talk to your system administrators
about how to get HTTP traffic from the world into your server.

Memory (RAM)
============

RAM is often the biggest limiting factor to the question 'how many users can use this JupyterHub
at the same time?'. If you want to support ``N`` maximum concurrent active users
each able to use up to ``X`` GB of RAM, you will need:

.. math::

    Server RAM = ($N \times X) + 128MB

The 128MB buffer is for system services (including JupyterHub itself).
This will guarantee that your server will not run out of RAM as long
as you have no more than ``N`` active users.
