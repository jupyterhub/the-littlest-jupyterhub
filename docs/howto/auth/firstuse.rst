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

.. code-block:: bash

   sudo tljh-config set auth.type firstuseauthenticator.FirstUseAuthenticator
   sudo tljh-config reload

Users who are currently logged in will continue to be logged in. When they
log out and try to log back in, they will be asked to provide a username and
password.

Users changing their own password
=================================

Users can change their password by first logging into their account and then visiting
the url ``<your_server_ip>/hub/auth/change-password``.

Allowing anyone to log in to your JupyterHub
============================================

By default, you need to manually create user accounts before they will be able
to log in to your JupyterHub. If you wish to allow **any** user to access
the JupyterHub, run the following command.

.. code-block:: bash

   tljh-config set auth.FirstUseAuthenticator.create_users true
   tljh-config reload


Resetting user password
=======================

The admin can reset user passwords by *deleting* the user from the JupyterHub admin
page. This logs the user out, but does **not** remove any of their data or
home directories. The user can then set a new password by logging in again with
their new password.

#. As an admin user, open the **Control Panel** by clicking the control panel
   button on the top right of your JupyterHub.

   .. image:: ../../images/control-panel-button.png
      :alt: Control panel button in notebook, top right

#. In the control panel, open the **Admin** link in the top left.

   .. image:: ../../images/admin/admin-access-button.png
      :alt: Admin button in control panel, top left

   This opens up the JupyterHub admin page, where you can add / delete users,
   start / stop peoples' servers and see who is online.

#. **Delete** the user whose password needs resetting. Remember this **does not**
   delete their data or home directory.

   .. image:: ../../images/auth/firstuse/delete-user.png
      :alt: Delete user button for each user

   If there is a confirmation dialog, confirm the deletion. This will also log the
   user out if they were currently running.

#. Re-create the user whose password needs resetting within that same dialog.

#. Ask the user to log in again with their new password as usual. This will be their
   new password going forward.
