=======================
The Littlest JupyterHub
=======================

.. image:: https://circleci.com/gh/jupyterhub/the-littlest-jupyterhub.svg?style=shield
   :target: https://circleci.com/gh/jupyterhub/the-littlest-jupyterhub
.. image:: https://codecov.io/gh/jupyterhub/the-littlest-jupyterhub/branch/master/graph/badge.svg
  :target: https://codecov.io/gh/jupyterhub/the-littlest-jupyterhub
.. image:: https://readthedocs.org/projects/the-littlest-jupyterhub/badge/?version=latest
   :target: https://the-littlest-jupyterhub.readthedocs.io
.. image:: https://badges.gitter.im/jupyterhub/jupyterhub.svg
   :target: https://gitter.im/jupyterhub/jupyterhub
.. image:: https://img.shields.io/badge/I_want_to_contribute!-grey?logo=jupyter
   :target: https://the-littlest-jupyterhub.readthedocs.io/en/latest/contributing/index.html

**The Littlest JupyterHub** (TLJH) distribution helps you provide Jupyter Notebooks
to 1-100 users on a single server.

The primary audience are people who do not consider themselves 'system administrators'
but would like to provide hosted Jupyter Notebooks for their students or users.
All users are provided with the same environment, and administrators
can easily install libraries into this environment without any specialized knowledge.

See the `latest documentation <https://the-littlest-jupyterhub.readthedocs.io>`_
for more information on using The Littlest JupyterHub.

For support questions please search or post to `our forum <https://discourse.jupyter.org/c/jupyterhub/>`_.

See the `contributing guide <https://the-littlest-jupyterhub.readthedocs.io/en/latest/contributing/index.html>`_
for information on the different ways of contributing to The Littlest JupyterHub.

See `this blog post <http://words.yuvi.in/post/the-littlest-jupyterhub/>`_ for
more information.


Development Status
==================

This project is currently in **beta** state. Folks have been using installations
of TLJH for more than a year now to great success. While we try hard not to, we
might still make breaking changes that have no clear upgrade pathway.

Installation
============

The Littlest JupyterHub (TLJH) can run on any server that is running at least
**Ubuntu 18.04**. Earlier versions of Ubuntu are not supported.
We have several tutorials to get you started.

- Tutorials to create a new server from scratch on a cloud provider & run TLJH
  on it. These are **recommended** if you do not have much experience setting up
  servers.

  - `Digital Ocean <https://the-littlest-jupyterhub.readthedocs.io/en/latest/install/digitalocean.html>`_
  - `OVH <https://the-littlest-jupyterhub.readthedocs.io/en/latest/install/ovh.html>`_
  - `Google Cloud <https://the-littlest-jupyterhub.readthedocs.io/en/latest/install/google.html>`_
  - `Jetstream <https://the-littlest-jupyterhub.readthedocs.io/en/latest/install/jetstream.html>`_
  - `Amazon Web Services <https://the-littlest-jupyterhub.readthedocs.io/en/latest/install/amazon.html>`_
  - `Microsoft Azure <https://the-littlest-jupyterhub.readthedocs.io/en/latest/install/azure.html>`_
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
