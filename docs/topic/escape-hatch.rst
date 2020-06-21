.. _topic/escape-hatch:


=============================
Custom configuration snippets
=============================

The two main TLJH components are **JupyterHub** and **Traefik**.

* JupyterHub takes its configuration from the ``jupyterhub_config.py`` file.
* Traefik loads its:
	* `static configuration <https://docs.traefik.io/v1.7/basics/#static-traefik-configuration>`_
	  from the ``traefik.toml`` file.
	* `dynamic configuration <https://docs.traefik.io/v1.7/basics/#dynamic-traefik-configuration>`_
	  from the ``rules`` directory.

The ``jupyterhub_config.py`` and ``traefik.toml`` files are created by TLJH during installation
and can be edited by the user only through ``tljh-config``. The ``rules`` directory is also created
during install along with a ``rules/rules.toml`` file, to be used by JupyterHub to store the routing
table from users to their notebooks.

.. note::
	Any direct modification to these files is unsupported, and will cause hard to debug issues.

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

Extending ``rules.toml``
========================

``Traefik`` is configured to load its routing table from the ``/opt/tljh/state/rules``
directory. The existing ``rules.toml`` file inside this directory is used by
``jupyterhub-traefik-proxy`` to add the JupyterHub routes from users to their notebook servers
and shouldn't be modified.

However, the routing table can be extended  outside JupyterHub's scope using the ``rules``
directory, by adding other dynamic configuration files with the desired routing rules.

.. note::
	* Any files in ``/opt/tljh/state/rules`` that end in ``.toml`` will be hot reload by Traefik.
	  This means that there is no need to reload the proxy service for the rules to take effect.

Checkout Traefik' docs about `dynamic configuration <https://docs.traefik.io/v1.7/basics/#dynamic-traefik-configuration>`_
and how to provide dynamic configuration through
`multiple separated files <https://docs.traefik.io/v1.7/configuration/backends/file/#multiple-separated-files>`_.
