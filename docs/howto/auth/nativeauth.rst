.. _howto/auth/nativeauth:

==============================================
Let users sign up with a username and password
==============================================

The **Native Authenticator** lets users signup for creating a new username 
and password.
When they signup, they won't be able to login until they are authorized by an 
admin. Users that are characterized as admin have to signup as well, but they  
will be authorized automatically.


Enabling the authenticator
==========================

Enable the authenticator and reload config to apply the configuration:

.. code-block:: bash

   sudo tljh-config set auth.type nativeauthenticator.NativeAuthenticator
   sudo tljh-config reload


Allowing all users to be authorized after signup
================================================

By default, all users created on signup don't have authorization to login. 
If you wish to allow **any** user to access
the JupyterHub just after the signup, run the following command:

.. code-block:: bash

   tljh-config set auth.NativeAuthenticator.open_signup true
   tljh-config reload

Optional features
=================

More optional features are available on the `authenticator documentation <https://native-authenticator.readthedocs.io/en/latest/>` 
