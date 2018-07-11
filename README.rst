=======================
The Littlest JupyterHub
=======================

.. image:: https://circleci.com/gh/yuvipanda/the-littlest-jupyterhub.svg?style=shield
   :target: https://circleci.com/gh/yuvipanda/the-littlest-jupyterhub
.. image:: https://media.readthedocs.org/static/projects/badges/passing-flat.svg
   :target: https://the-littlest-jupyterhub.readthedocs.io
.. image:: https://badges.gitter.im/jupyterhub/jupyterhub.svg
   :target: https://gitter.im/jupyterhub/jupyterhub

**The Littlest JupyterHub** (TLJH) distribution helps you provide Jupyter Notebooks
to 1-50 users on a single server.

Administrators who do not consider themselves 'system administrators' but would
like to provide hosted Jupyter Notebooks for their students / users are the
primary audience. All users get the same environment, and administrators can
install libraries into this environment without any specialized knowledge.
It provides all users with the same environment, and administrators can install
libraries into this environment easily without any specialized knowledge.

See `this blog post <http://words.yuvi.in/post/the-littlest-jupyterhub/>`_ for
more information.

Development Status
==================

This project is currently in **pre-alpha**, and things will break all the time.
However, feedback at this time is extremely valuble, so you should still try
it out!

Installation
============

The Littlest JupyterHub (TLJH) can run on any server that is running at least
Ubuntu 18.04. We have a bunch of tutorials to get you started!

- Tutorials to create a new server from scratch on a cloud provider & run TLJH
  on it. These are **recommended** if you do not have much experience setting up
  servers.

  - `Digital Ocean <http://the-littlest-jupyterhub.readthedocs.io/en/latest/tutorials/digitalocean.html>`_
  - `Google Cloud <http://the-littlest-jupyterhub.readthedocs.io/en/latest/tutorials/google.html>`_
  - `Jetstream <http://the-littlest-jupyterhub.readthedocs.io/en/latest/tutorials/jetstream.html>`_
  - ... your favorite provider here, if you can contribute!

- `Tutorial to install TLJH on an already running server you have root access to
  <http://the-littlest-jupyterhub.readthedocs.io/en/latest/tutorials/custom.html>`_.
  You should use this if your cloud provider does not already have a direct tutorial,
  or if you have experience setting up servers.
