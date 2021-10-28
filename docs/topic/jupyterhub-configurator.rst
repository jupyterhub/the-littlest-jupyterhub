.. _topic/jupyterhub-configurator:

=======================
JupyterHub Configurator
=======================

The `JupyterHub configurator <https://github.com/yuvipanda/jupyterhub-configurator>`_ allows admins to change a subset of hub settings via a GUI.

.. image:: ../images/jupyterhub-configurator.png
  :alt: Changing the default JupyterHub interface

Enabling the configurator
=========================

Because the configurator is under continue development and it might change over time, it is disabled by default in TLJH.
If you want to experiment with it, it can be enabled using ``tljh-config``:

.. code-block:: bash

    sudo tljh-config set services.configurator.enabled True
    sudo tljh-config reload

Accessing the Configurator
==========================

After enabling the configurator using ``tljh-config``, the service will only be available to hub admins, from within the control panel.
The configurator can be accessed from under ``Services`` in the top navigation bar. It will ask to authenticate, so it knows the user is an admin.
Once done, the configurator interface will be available.
