.. _contributing/dev-setup:

==================================
Setting up Development Environment
==================================

The easiest & safest way to develop & test TLJH is with `Docker <https://www.docker.com/>`_.

#. Install Docker Community Edition by following the instructions on
   `their website <https://www.docker.com/community-edition>`_.

#. Clone the `git repo <https://github.com/jupyterhub/the-littlest-jupyterhub>`_ (or your fork of it).
#. Build a docker image that has a functional systemd in it.

   .. code-block:: bash

      docker build -t tljh-systemd . -f integration-tests/Dockerfile

#. Run a docker container with the image in the background, while bind mounting
   your TLJH repository under ``/srv/src``.

   .. code-block:: bash

      docker run \
        --privileged \
        --detach \
        --name=tljh-dev \
        --publish 12000:80 \
        --mount type=bind,source=$(pwd),target=/srv/src \
        tljh-systemd

#. Get a shell inside the running docker container.

   .. code-block:: bash

      docker exec -it tljh-dev /bin/bash

#. Run the bootstrapper from inside the container (see step above):
   The container image is already set up to default to a ``dev`` install, so
   it'll install from your local repo rather than from github.

   .. code-block:: console

      python3 /srv/src/bootstrap/bootstrap.py --admin admin

  Or, if you would like to setup the admin's password during install,
  you can use this command (replace "admin" with the desired admin username
  and "password" with the desired admin password):

   .. code-block:: console

      python3 /srv/src/bootstrap/bootstrap.py --admin admin:password

   The primary hub environment will also be in your PATH already for convenience.

#. You should be able to access the JupyterHub from your browser now at
   `http://localhost:12000 <http://localhost:12000>`_. Congratulations, you are
   set up to develop TLJH!

#. Make some changes to the repository. You can test easily depending on what
   you changed.

   * If you changed the ``bootstrap/bootstrap.py`` script or any of its dependencies,
     you can test it by running ``python3 /srv/src/bootstrap/bootstrap.py``.

   * If you changed the ``tljh/installer.py`` code (or any of its dependencies),
     you can test it by running ``python3 -m tljh.installer``.

   * If you changed ``tljh/jupyterhub_config.py``, ``tljh/configurer.py``,
     ``/opt/tljh/config/`` or any of their dependencies, you only need to
     restart jupyterhub for them to take effect. ``tljh-config reload hub``
     should do that.

:ref:`troubleshooting/logs` has information on looking at various logs in the container
to debug issues you might have.
