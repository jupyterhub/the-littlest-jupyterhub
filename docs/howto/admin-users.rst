.. _howto/admin-users:

========================
Add / Remove admin users
========================

Admin users in TLJH have the following powers:

#. Full root access to the server with passwordless ``sudo``.
   This lets them do literally whatever they want in the server
#. Access servers / home directories of all other users
#. Install new packages for everyone with ``conda``, ``pip`` or ``apt``
#. Change configuration of TLJH

This is a lot of power, so make sure you know who you are giving it
to. Admin users should have decent passwords / secure logni mechanisms,
so attackers can not easily gain control of the system.

Make sure an admin user is present
==================================

You should make sure an admin user is present when you **install** TLJH
the very first time. The ``:ref:`--admin <topic/customizing-installer/admin>```
flag passed to the installer does this. If you had forgotten to do so, the
easiest way to fix this is to run the installer again.

Adding new admin users
======================

New admin users can be added by executing the following commands on an
admin terminal:

.. code-block:: bash

   sudo -E tljh-config add-item users.admin <username>
   sudo -E tljh-config reload

If the user is already using the JupyterHub, they might have to stop and
start their server from the control panel to gain new powers.

Removing admin users
====================

You can remove an existing admin user by executing the following commands in
an admin terminal:

.. code-block:: bash

   sudo -E tljh-config remove-item users.admin <username>
   sudo -E tljh-config reload

If the user is already using the JupyterHub, they will continue to have
some of their admin powers until their server is stopped. Another admin
can force their server to stop by clicking 'Stop Server' in the admin
panel.
