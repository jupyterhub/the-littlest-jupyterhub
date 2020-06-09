.. _topic/escape-hatch:


=============================
Custom configuration snippets
=============================

The two main TLJH components are **JupyterHub** and **Traefik**.

* JupyterHub takes its configuration from the ``jupyterhub_config.py`` file.
* Traefik takes its configuration from the ``traefik.toml`` file.

These files are created by TLJH during installation and can be edited by the
user only through ``tljh-config``. Any direct modification to these files,
is unsupported, and will cause hard to debug issues.

But because sometimes TLJH needs to be customized in ways that are not officially
supported, an escape hatch has been introduced to allow easily extending the
configuration. Please follow the sections below for how to extend JupyterHub's
and Traefik's configuration outside of ``tljh-config`` scope.

Extending ``jupyterhub_config.py``
==================================

The ``jupyterhub_config.d`` directory lets you load multiple ``jupyterhub_config.py``
snippets for your configuration.

* 	Any files in ``/opt/tljh/config/jupyterhub_config.d`` that end in ``.py`` will
	be loaded in alphabetical order as python files to provide configuration for
	JupyterHub.
* 	The configuration files can have any name, but they need to have the `.py`
	extension and to respect this format.
* 	Any config that can go in a regular ``jupyterhub_config.py`` file is valid in
	these files.
* 	They will be loaded *after* any of the config options specified with ``tljh-config``
	are loaded.

Once you have created and defined your custom JupyterHub config file/s, just reload the
hub for the new configuration to take effect:

.. code-block:: bash

	sudo tljh-config reload hub


Extending ``traefik.toml``
==========================

The ``traefik_config.d`` directory lets you load multiple ``traefik.toml``
snippets for your configuration.

*	Any files in ``/opt/tljh/config/traefik_config.d`` that end in ``.toml`` will be
	loaded in alphabetical order to provide configuration for Traefik.
*	The configuration files can have any name, but they need to have the `.toml`
	extension and to respect this format.
*	Any config that can go in a regular ``traefik.toml`` file is valid in these files.
*	They will be loaded *after* any of the config options specified with ``tljh-config``
	are loaded.

Once you have created and defined your custom Traefik config file/s, just reload the
proxy for the new configuration to take effect:

.. code-block:: bash

	sudo tljh-config reload proxy

.. warning:: This instructions might change when TLJH will switch to Traefik > 2.0
