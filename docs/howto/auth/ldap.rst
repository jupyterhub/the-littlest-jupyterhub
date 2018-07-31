.. _howto/auth/ldap:

=============================
Using LDAP for authentication
=============================

`LDAP <https://en.wikipedia.org/wiki/Lightweight_Directory_Access_Protocol>`_
is an open and widely-used protocol for authentication.

The `LDAPAuthenticator's documentation <https://github.com/jupyterhub/ldapauthenticator#required-configuration>`_
lists the various configuration options you can set for LDAPAuthenticator. You can set them
in TLJH with the following pattern:

.. code-block:: bash

   sudo -E tljh-config set auth.<authenticator-name>.<config-option-name> <config-option-value>

When the documentation asks you to set ``LDAPAuthenticator.server_address`` to some
value, you can do that with the following command:

.. code-block:: bash

   sudo -E tljh-config set auth.LDAPAuthenticator.server_address = 'my-ldap-server'

Enabling the authenticator
==========================

For LDAPAuthenticator, the fully qualified name is ``ldapauthenticator.LDAPAuthenticator``.
This is the same name that the `documentation asks <https://github.com/jupyterhub/ldapauthenticator#usage>`_
you to set ``c.JupyterHub.authenticator_class`` to.

For LDAPAuthenticator, this would be:

.. code-block:: bash

   sudo -E tljh-config set auth.type ldapauthenticator.LDAPAuthenticator

Once enabled, you need to reload JupyterHub for the config to take effect.

.. code-block:: bash

   sudo -E tljh-config reload

Try logging in a separate incognito window to check if your configuration works. This
lets you preserve your terminal in case there were errors. If there are
errors, :ref:`troubleshooting/logs` should help you debug them.
