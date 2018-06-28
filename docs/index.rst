The Littlest JupyterHub
-----------------------

A simple `JupyterHub <https://github.com/jupyterhub/jupyterhub>`_ distribution for
a small (0-50) number of users on a single server.

Quick Start
===========

On a fresh Ubuntu 18.04 server, you can install The Littlest JupyterHub with:

.. code-block:: bash

   curl https://raw.githubusercontent.com/yuvipanda/the-littlest-jupyterhub/master/installer/install.bash | sudo bash -

This takes 2-5 minutes to run. When completed, you can access your new JupyterHub
at the public IP of your server!

If this installation method (``curl <arbitrary-url> | sudo bash -``)
makes you nervous, check out the :ref:`other installation methods <installation>` we support!

Tutorials
=========

Tutorials guide you through accomplishing specific goals. Great place to get
started!

.. toctree::
   :titlesonly:

   tutorials/quickstart

Guides
======

Guides provide in-depth explanations of specific topics.

.. toctree::
   :titlesonly:

   guides/requirements
   guides/install
   guides/admin
