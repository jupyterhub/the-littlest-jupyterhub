=======================
Security Considerations
=======================

The Littlest JupyterHub is in beta state & should not be used in security
critical situations. We will try to keep things as secure as possible, but
sometimes trade security for massive gains in convenience. This page contains
information about the security model of The Littlest JupyterHub.

System user accounts
====================

Each JupyterHub user gets their own Unix user account created when they
first start their server. This protects users from each other, gives them a
home directory at a well known location, and allows sharing based on file system
permissions.

#. The unix user account created for a JupyterHub user named ``<username>`` is
   ``jupyter-<username>``. This prefix helps prevent clashes with users that
   already exist - otherwise a user named ``root`` can trivially gain full root
   access to your server. If the username (including the ``jupyter-`` prefix)
   is longer than 26 characters, it is truncated at 26 characters & a 5 charcter
   hash is appeneded to it. This keeps usernames under the linux username limit
   of 32 characters while also reducing chances of collision.

#. A home directory is created for the user under ``/home/jupyter-<username>``.

#. The default permission of the home directory is change with ``o-rwx`` (remove
   non-group members the ability to read, write or list files and folders in the
   Home directory).

#. No password is set for this unix system user by default. The password used
   to log in to JupyterHub (if using an authenticator that requires a password)
   is not related to the unix user's password in any form.

#. All users created by The Littlest JupyterHub are added to the user group
   ``jupyterhub-users``.

``sudo`` access for admins
==========================

JupyterHub admin users are added to the user group ``jupyterhub-admins``,
which is granted complete root access to the whole server with the ``sudo``
command on the terminal. No password required.

This is a **lot** of power, and they can do pretty much anything they want to
the server - look at other people's work, modify it, break the server in cool &
funky ways, etc. This also means **if an admin's credentials are compromised 
(easy to guess password, password re-use, etc) the entire JupyterHub is compromised.**

Off-boarding users securely
===========================

When you delete users from the JupyterHub admin console, their unix user accounts
are **not** removed. This means they might continue to have access to the server
even after you remove them from JupyterHub. Admins should manually remove the user
from the server & archive their home directories as needed. For example, the
following command deletes the unix user associated with the JupyterHub user ``yuvipanda``.

.. code-block:: bash

   sudo userdel jupyter-yuvipanda

If the user removed from the server is an admin, extra care must be taken
since they could have modified the system earlier to continue giving them
access.

Per-user ``/tmp``
=================

``/tmp`` is shared by all users in most computing systems, and this has been
a consistent source of security issues. The Littlest JupyterHub gives each
user their own ephemeral ``/tmp`` using the `PrivateTmp <https://www.freedesktop.org/software/systemd/man/systemd.exec.html#PrivateTmp>`_
feature of systemd.

HTTPS
=====

Any internet-facing JupyterHub should use HTTPS to secure its traffic. For
information on how to use HTTPS with your JupyterHub, see :ref:`howto/admin/https`.
