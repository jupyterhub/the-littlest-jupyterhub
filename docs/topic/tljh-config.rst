.. _topic/tljh-config:

=====================================
Configuring TLJH with ``tljh-config``
=====================================

``tljh-config`` is the commandline program used to make configuration
changes to TLJH. 

Running ``tljh-config``
======================`

You can run ``tljh-config`` in two ways:

#. From inside a terminal in JupyterHub while logged in as an admin user.
   This method is **recommended**.

#. By directly calling ``/opt/tljh/hub/bin/tljh-config`` as root when
   logged in to the server via other means (such as SSH). This is an
   advanced use case, and not covered much in this guide.

Set a configuration property
============================

TLJH's configuration is organized in a nested tree structure. You can
set a particular property with the following command:

.. code-block:: bash

   sudo -E tljh-config set <property-path> <value>


where:

#. ``<property-path>`` is a dot-separated path to the property you want
   to set.
#. ``<value>`` is the value you want to set the property to.

For example, to set the password for the DummyAuthenticator, you
need to set the ``auth.DummyAuthenticator.password`` property. You would
do so with the following:

.. code-block:: bash

   sudo -E tljh-config set auth.DummyAuthenticator.password mypassword


This can only set string and numerical properties, not lists.

View current configuration
==========================

To see the current configuration, you can run the following command:

.. code-block:: bash

   sudo -E tljh-config show

This will print the current configuration of your TLJH. This is very
useful when asking for support!

Reloading JupyterHub to apply configuration
===========================================

After modifying the configuration, you need to reload JupyterHub for
it to take effect. You can do so with:

.. code-block:: bash

   sudo -E tljh-config reload

This should not affect any running users. The JupyterHub will be
restarted and loaded with the new configuration.

Advanced: ``config.yaml``
=========================

``tljh-config`` is a simple program that modifies the contents of the 
``config.yaml`` file located at ``/opt/tljh/config.yaml``. ``tljh-config`` 
is the recommended method of editing / viewing configuration since editing
YAML by hand in a terminal text editor is a large source of errors.