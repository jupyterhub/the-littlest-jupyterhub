.. _howto/auth/dummy:

=====================================================
Authenticate *any* user with a single shared password
=====================================================

The **Dummy Authenticator** lets *any* user log in with the given password.
This authenticator is **extremely insecure**, so do not use it if you can
avoid it.

Enabling the authenticator
==========================

1. Always use DummyAuthenticator with a password. You can communicate this
   password to all your users via an out of band mechanism (like writing on
   a whiteboard). Once you have selected a password, configure TLJH to use
   the password by executing the following from an admin console.

   .. code-block:: bash

      sudo tljh-config set auth.DummyAuthenticator.password <password>

   Remember to replace ``<password>`` with the password you choose.

2. Enable the authenticator and reload config to apply configuration:

   .. code-block:: bash

      sudo tljh-config set auth.type dummy

   .. code-block:: bash

      sudo tljh-config reload

Users who are currently logged in will continue to be logged in. When they
log out and try to log back in, they will be asked to provide a username and
password.

Changing the password
=====================

The password used by DummyAuthenticator can be changed with the following
commands:

.. code-block:: bash

   tljh-config set auth.DummyAuthenticator.password <new-password>

.. code-block:: bash

   tljh-config reload
