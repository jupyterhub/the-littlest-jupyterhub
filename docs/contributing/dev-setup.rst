.. _contributing/dev-setup:

==================================
Setting up Development Environment
==================================

The easiest & safest way to develop & test TLJH is with `Docker <https://www.docker.com/>`_.

#. Install Docker Community Edition by following the instructions on
   `their website <https://www.docker.com/community-edition>`_.

#. Clone the `git repo <https://github.com/jupyterhub/the-littlest-jupyterhub>`_ (or your fork of it).
#. Build the Docker image and start the container.

   .. code-block:: bash

      docker-compose up --build

#. From another terminal, run the bootstrapper:
   The container image is already set up to default to a ``dev`` install, so
   it'll install from your local repo rather than from github.

   .. code-block:: bash

      docker-compose exec hub python3 /srv/src/bootstrap/bootstrap.py --admin admin

  Or, if you would like to setup the admin's password during install,
  you can use this command (replace "admin" with the desired admin username
  and "password" with the desired admin password):

   .. code-block:: bash

      docker-compose exec hub python3 /srv/src/bootstrap/bootstrap.py --admin admin:password

   The primary hub environment will also be in your PATH already for convenience.

#. You should be able to access the JupyterHub from your browser now at
   `http://localhost:12000 <http://localhost:12000>`_. Congratulations, you are
   set up to develop TLJH!

#. Make some changes to the repository. You can test easily depending on what
   you changed.

   * If you changed the ``bootstrap/bootstrap.py`` script or any of its dependencies,
     you can test it by running:

      .. code-block:: bash

         docker-compose exec hub python3 /srv/src/bootstrap/bootstrap.py

   * If you changed the ``tljh/installer.py`` code (or any of its dependencies),
     you can test it by running:

      .. code-block:: bash

         docker-compose exec hub python3 -m tljh.installer

   * If you changed ``tljh/jupyterhub_config.py``, ``tljh/configurer.py``,
     ``/opt/tljh/config/`` or any of their dependencies, you only need to
     restart jupyterhub for them to take effect:

      .. code-block:: bash

         docker-compose exec hub tljh-config reload hub

:ref:`troubleshooting/logs` has information on looking at various logs in the container
to debug issues you might have.
