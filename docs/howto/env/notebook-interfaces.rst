.. _howto/env/notebook_interfaces:

=======================================
Change default User Interface for users
=======================================

By default, logging into TLJH puts you in the classic Jupyter Notebook interface
we all know and love. However, there are at least two other popular notebook
interfaces you can use:

1. `JupyterLab <http://jupyterlab.readthedocs.io/en/stable/>`_
2. `nteract <https://nteract.io/>`_

Both these interfaces are also shipped with tljh by default. You can try them
temporarily, or set them to be the default interface whenever you login.

Trying an alternate interface temporarily
=========================================

When you log in & start your server, by default the URL in your browser
will be something like ``/user/<username>/tree``. The ``/tree`` is what tells
the notebook server to give you the classic notebook interface.

* **For the JupyterLab interface**: change ``/tree`` to ``/lab``.
* **For the nteract interface**: change ``/tree`` to ``/nteract``

You can play around with them and see what fits your use cases best.

Changing the default user interface
===================================

You can change the default interface users get when they log in by modifying
``config.yaml`` as an admin user.

#. To launch **JupyterLab** when users log in, run the following in an admin console:

   .. code-block:: yaml

      sudo tljh-config set user_environment.default_app jupyterlab

#. Alternatively, to launch **nteract** when users log in, run the following in the admin console:

   .. code-block:: yaml

      sudo tljh-config set user_environment.default_app nteract

#. Apply the changes by restarting JupyterHub. This should not disrupt current users.

   .. code-block:: yaml

      sudo tljh-config reload hub

   If this causes problems, check the :ref:`troubleshoot_logs_jupyterhub` for clues
   on what went wrong.

Users might have to restart their servers from control panel to get the new interface.
