
=============================================
Stopping and Restarting the JupyterHub Server
=============================================

The user can **stop** the JupyterHub server using:

.. code-block:: console

     $ systemctl stop jupyterhub.service

.. warning:: 

    Keep in mind that other services that may also require stopping:

    * The user's Jupyter server: jupyter-username.service
    * Traefik.service

The user may **restart** JupyterHub and Traefik services by running:

.. code-block:: console

     $ sudo tljh-config reload proxy

This calls systemctl and restarts Traefik. The user may call systemctl and restart only the JupyterHub using the command: 

.. code-block:: console

     $ sudo tljh-config reload hub
