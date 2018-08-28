.. _topic/escape-hatch:

========================================
Custom ``jupyterhub_config.py`` snippets
========================================

Sometimes you need to customize TLJH in ways that are not officially supported.
We provide an easy escape hatch for those cases with a ``jupyterhub_conf.d``
directory that lets you load multiple ``jupyterhub_config.py`` snippets for
your configuration. You need to create the directory when you use it for
the first time.

Any files in ``/opt/tljh/config/jupyterhub_config.d`` that end in ``.py`` will be
loaded in alphabetical order as python files to provide configuration for
JupyterHub. Any config that can go in a regular ``jupyterhub_config.py``
file is valid in these files. They will be loaded *after* any of the config
options specified with ``tljh-config`` are loaded.
