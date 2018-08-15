=======================
The Littlest JupyterHub
=======================

.. image:: https://circleci.com/gh/jupyterhub/the-littlest-jupyterhub.svg?style=shield
   :target: https://circleci.com/gh/jupyterhub/the-littlest-jupyterhub
.. image:: https://codecov.io/gh/jupyterhub/the-littlest-jupyterhub/branch/master/graph/badge.svg
  :target: https://codecov.io/gh/jupyterhub/the-littlest-jupyterhub
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

This project is currently in **alpha** state. Most things work, but we might
still make breaking changes that have no clear upgrade pathway. We are targetting
a v0.1 release sometime in mid-August 2018. Follow `this milestone <https://github.com/jupyterhub/the-littlest-jupyterhub/milestone/1>`_
to see progress towards the release!

Installation
============

The Littlest JupyterHub (TLJH) can run on any server that is running at least
Ubuntu 18.04. We have a bunch of tutorials to get you started!

- Tutorials to create a new server from scratch on a cloud provider & run TLJH
  on it. These are **recommended** if you do not have much experience setting up
  servers.

  - `Digital Ocean <https://the-littlest-jupyterhub.readthedocs.io/en/latest/install/digitalocean.html>`_
  - `Google Cloud <https://the-littlest-jupyterhub.readthedocs.io/en/latest/install/google.html>`_
  - `Jetstream <https://the-littlest-jupyterhub.readthedocs.io/en/latest/install/jetstream.html>`_
  - ... your favorite provider here, if you can contribute!

- `Tutorial to install TLJH on an already running server you have root access to
  <https://the-littlest-jupyterhub.readthedocs.io/en/latest/install/custom-server.html>`_.
  You should use this if your cloud provider does not already have a direct tutorial,
  or if you have experience setting up servers.

Documentation
=============

Our latest documentation is at: https://the-littlest-jupyterhub.readthedocs.io

We place a high importance on consistency, readability and completeness of
documentation. If a feature is not documented, it does not exist. If a behavior
is not documented, it is a bug! We try to treat our documentation like we treat
our code: we aim to improve it as often as possible.

If something is confusing to you in the documentation, it is a bug. We would be
happy if you could `file an issue
<https://github.com/jupyterhub/the-littlest-jupyterhub/issues>`_ about it - or
even better, `contribute a documentation fix
<http://the-littlest-jupyterhub.readthedocs.io/en/latest/contributing/docs.html>`_!
