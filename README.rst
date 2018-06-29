The Littlest JupyterHub
=======================

.. image:: https://circleci.com/gh/yuvipanda/the-littlest-jupyterhub.svg?style=shield
   :target: https://circleci.com/gh/yuvipanda/the-littlest-jupyterhub
.. image:: https://media.readthedocs.org/static/projects/badges/passing-flat.svg
   :target: https://the-littlest-jupyterhub.readthedocs.io
.. image:: https://badges.gitter.im/jupyterhub/jupyterhub.svg
   :target: https://gitter.im/jupyterhub/jupyterhub

A simple JupyterHub distribution for 1-50 users on a single server.

This project is currently in pre-alpha state & extremely prone to breaking!

See `this blog post <http://words.yuvi.in/post/the-littlest-jupyterhub/>`_ for
more information.

Quick Start
-----------

On a fresh Ubuntu 18.04 server, you can install The Littlest JupyterHub with:

.. code-block:: bash

   curl https://raw.githubusercontent.com/yuvipanda/the-littlest-jupyterhub/master/installer/install.bash | sudo bash -

This takes 2-5 minutes to run. When completed, you can access your new JupyterHub
at the public IP of your server (on the default http port 80)!

For more information (including other installation methods), check out the
`documentation <https://the-littlest-jupyterhub.readthedocs.io>`_.
