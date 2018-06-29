.. _contributing_dev_setup:

Setting up Development Environment
==================================

The easiest & safest way to develop & test TLJH is with `Docker <https://www.docker.com/>`_.

#. Install Docker Community Edition by following the instructions on
   `their website <https://www.docker.com/community-edition>`_.

#. Clone the git repo (or your fork of it).
#. Build a docker image that has a functional systemd in it.

   .. code-block:: bash

      sudo docker build -t tljh-systemd .

#. Run a docker container with the image in the background, while bind mounting
   your TLJH repository under ``/srv/src``.

   .. code-block:: bash

      sudo docker run \
        --privileged \
        --detach \
        --name=tljh-dev \
        --publish 12000:80 \
        --mount type=bind,source=$(pwd),target=/srv/src \
        tljh-systemd

#. Get a shell inside the running docker container.

   .. code-block:: bash

      sudo docker exec -it tljh-dev /bin/bash

#. Run the installer from inside the container (see step above): 
   The container image is already set up to default to a ``dev`` install, so 
   it'll install from your local repo rather than from github.

   .. code-block:: console

      bash /srv/src/installer/install.bash

   The primary hub environment will also be in your PATH already for convenience.

#. You should be able to access the JupyterHub from your browser now at
   `http://localhost:12000 <http://localhost:12000>`_. Congratulations, you are
   set up to develop TLJH!

#. Make some changes to the repository. You can test easily depending on what
   you changed.

   * If you changed the ``installer/install.bash`` script or any of its dependencies,
     you can test it by running ``bash /srv/src/installer/install.bash``.

   * If you changed the ``tljh/installer.py`` code (or any of its dependencies),
     you can test it by running ``python3 -m tljh.installer``.

   * If you changed ``tljh/jupyterhub_config.py``, ``tljh/configurer.py``,
     ``/opt/tljh/config.yaml`` or any of their dependencies, you only need to
     restart jupyterhub for them to take effect. ``systemctl restart jupyterhub``
     should do that.

:ref:`troubleshoot_logs` has information on looking at various logs in the container
to debug issues you might have.
