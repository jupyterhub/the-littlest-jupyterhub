.. _admin_access:

Administrative Access
---------------------

In The Littlest JupyterHub, we try to allow users to do as many administrative
tasks as possible within JupyterHub itself. Admin users can:

1. Have full root access with passwordless ``sudo``
2. Install system-wide packages with ``apt``
3. Install ``conda`` / ``pip`` packages for all JupyterHub users
4. Change the amount of RAM / CPU available to each user, and more!

By default, there are no admin users. You should add some after installation.

Adding admin users
==================

Admin users are specified in the `YAML <https://en.wikipedia.org/wiki/YAML>`_
config file at ``/opt/tljh/config.yaml``. This file is created upon installing
tljh.

1. Open the ``config.yaml`` file for editing.

   .. code-block:: bash

      sudo nano /opt/tljh/config.yaml

2. Add usernames that should have admin access.

   .. code-block:: yaml

      users:
        admin:
          - user1
          - user2

   Be careful around the syntax - indentation matters, and you should be using
   spaces and not tabs.

   When you are done, save the file and exit. In ``nano``, you can do this with
   ``Ctrl+X`` key.

3. When you are sure the format is ok, restart JupyterHub to let the config take
   effect.

   .. code-block:: bash

      sudo systemctl restart jupyterhub

This should give you admin access from JupyterHub! You can verify this by:

1. Opening a Terminal in your JupyterHub and checking if ``sudo`` works
2. Opening your JupyterHub ``Control Panel`` and checking for the **Admin** tab

From now on, you can use the JupyterHub to do most configuration changes.
