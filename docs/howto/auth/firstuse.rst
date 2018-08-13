.. _howto/auth/firstuse:

==================================================
Let users choose a password when they first log in
==================================================

The **First Use Authenticator** lets users choose their own password.
Upon their first log-in attempt, whatever password they use will be stored
as their password for subsequent log in attempts. This is
the default authenticator that ships with TLJH.

Enabling the authenticator
==========================

.. note:: the FirstUseAuthenticator is enabled by default in TLJH.

#. Enable the authenticator and reload config to apply the configuration:

   sudo tljh-config set auth.type firstuseauthenticator.FirstUseAuthenticator
   sudo tljh-config reload

Users who are currently logged in will continue to be logged in. When they
log out and try to log back in, they will be asked to provide a username and
password.

Allowing anyone to log in to your JupyterHub
============================================

By default, you need to manually create user accounts before they will be able
to log in to your JupyterHub. If you wish to allow **any** user to access
the JupyterHub, run the following command.

.. code-block:: bash

   tljh-config set auth.FirstUseAuthenticator.create_users true
   tljh-config reload
