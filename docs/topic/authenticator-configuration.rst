.. _topic/authenticator-configuration:

=====================================
Configuring JupyterHub authenticators
=====================================

Any `JupyterHub authenticator <https://github.com/jupyterhub/jupyterhub/wiki/Authenticators>`_
can be used with TLJH. A number of them ship by default with TLJH:

#. `OAuthenticator <https://github.com/jupyterhub/oauthenticator>`_ - Google, GitHub, CILogon,
   GitLab, Globus, Mediawiki, auth0, generic OpenID connect (for KeyCloak, etc) and other
   OAuth based authentication methods.
#. `LDAPAuthenticator <https://github.com/jupyterhub/ldapauthenticator>`_ - LDAP & Active Directory.
#. `DummyAuthenticator <https://github.com/yuvipanda/jupyterhub-dummy-authenticator>`_ - Any username,
   one shared password. A :ref:`how-to guide on using DummyAuthenticator <howto/auth/dummy>` is also
   available.
#. `FirstUseAuthenticator <https://github.com/yuvipanda/jupyterhub-firstuseauthenticator>`_ - Users set
   their password when they log in for the first time. Default authenticator used in TLJH.
#. `TmpAuthenticator <https://github.com/jupyterhub/tmpauthenticator>`_ - Opens the JupyterHub to the
   world, makes a new user every time someone logs in.
#. `NativeAuthenticator <https://native-authenticator.readthedocs.io/en/latest/>`_ - Allow users to signup, add password security verification and block users after failed attempts oflogin. 

We try to have specific how-to guides & tutorials for common authenticators. Since we can not cover
everything, this guide shows you how to use any authenticator you want with JupyterHub by following
the authenticator's documentation.

Setting authenticator properties
================================

JupyterHub authenticators are customized by setting *traitlet properties*. In the authenticator's
documentation, you will find these are usually represented as:

.. code-block:: python

   c.<AuthenticatorName>.<property-name> = <some-value>

You can set these with ``tljh-config`` with:

.. code-block:: bash

   sudo tljh-config set auth.<AuthenticatorName>.<property-name> <some-value>

Example
-------

`LDAPAuthenticator's documentation <https://github.com/jupyterhub/ldapauthenticator#required-configuration>`_
lists the various configuration options you can set for LDAPAuthenticator.
When the documentation asks you to set ``LDAPAuthenticator.server_address``
to some value, you can do that with the following command:

.. code-block:: bash

   sudo tljh-config set auth.LDAPAuthenticator.server_address 'my-ldap-server'

Most authenticators require you set multiple configuration options before you can
enable them. Read the authenticator's documentation carefully for more information.

Enabling the authenticator
==========================

Once you have configured the authenticator as you want, you should then
enable it. Usually, the documentation for the authenticator would ask you to add
something like the following to your ``jupyterhub_config.py`` to enable it:

.. code-block:: python

   c.JupyterHub.authenticator_class = 'fully-qualified-authenticator-name'

You can accomplish the same with ``tljh-config``:

.. code-block:: bash

   sudo tljh-config set auth.type <fully-qualified-authenticator-name>

Once enabled, you need to reload JupyterHub for the config to take effect.

.. code-block:: bash

   sudo tljh-config reload

Try logging in a separate incognito window to check if your configuration works. This
lets you preserve your terminal in case there were errors. If there are
errors, :ref:`troubleshooting/logs` should help you debug them.

Example
-------

From the `documentation <https://github.com/jupyterhub/ldapauthenticator#usage>`_ for
LDAPAuthenticator, we see that the fully qualified name is ``ldapauthenticator.LDAPAuthenticator``.
Assuming you have already configured it, the following commands enable LDAPAuthenticator.

.. code-block:: bash

   sudo tljh-config set auth.type ldapauthenticator.LDAPAuthenticator
   sudo tljh-config reload
