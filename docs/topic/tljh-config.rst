.. _topic/tljh-config:

=====================================
Configuring TLJH with ``tljh-config``
=====================================

``tljh-config`` is the commandline program used to make configuration
changes to TLJH.

Running ``tljh-config``
=======================

You can run ``tljh-config`` in two ways:

#. From inside a terminal in JupyterHub while logged in as an admin user.
   This method is recommended.

#. By directly calling ``/opt/tljh/hub/bin/tljh-config`` as root when
   logged in to the server via other means (such as SSH). This is an
   advanced use case, and not covered much in this guide.

.. _tljh-set:


Set / Unset a configuration property
====================================

TLJH's configuration is organized in a nested tree structure. You can
set a particular property with the following command:

.. code-block:: bash

   sudo tljh-config set <property-path> <value>


where:

#. ``<property-path>`` is a dot-separated path to the property you want
   to set.
#. ``<value>`` is the value you want to set the property to.

For example, to set the password for the DummyAuthenticator, you
need to set the ``auth.DummyAuthenticator.password`` property. You would
do so with the following:

.. code-block:: bash

   sudo tljh-config set auth.DummyAuthenticator.password mypassword


This can only set string and numerical properties, not lists.

To unset a configuration property you can use the following command:

.. code-block:: bash

   sudo tljh-config unset <property-path>

Unsetting a configuration property removes the property from the configuration
file. If what you want is only to change the property's value, you should use
``set`` and overwrite it with the desired value.


Some of the existing ``<property-path>`` are listed below by categories:

.. _tljh-base_url:

Base URL
--------

    Use ``base_url`` to determine the base URL used by JupyterHub. This parameter will 
    be passed straight to ``c.JupyterHub.base_url``.

.. _tljh-set-auth:

Authentication
--------------

    Use ``auth.type`` to determine authenticator to use. All parameters
    in the config under ``auth.{auth.type}`` will be passed straight to the
    authenticators themselves.
    
.. _tljh-set-ports:

Ports
-----

  Use ``http.port`` and ``https.port`` to set the ports that TLJH will listen on, 
  which are 80 and 443 by default. However, if you change these, note that 
  TLJH does a lot of other things to the system (with user accounts and sudo
  rules primarily) that might break security assumptions your other 
  applications have, so use with extreme caution.
  
  .. code-block:: bash

    sudo tljh-config set http.port 8080
    sudo tljh-config set https.port 8443
    sudo tljh-config reload proxy

.. _tljh-set-user-lists:

User Lists
----------


* ``users.allowed`` takes in usernames to whitelist

* ``users.banned`` takes in usernames to blacklist

* ``users.admin`` takes in usernames to designate as admins

  .. code-block:: bash

    sudo tljh-config add-item users.allowed good-user_1
    sudo tljh-config add-item users.allowed good-user_2
    sudo tljh-config add-item users.banned bad-user_6
    sudo tljh-config add-item users.admin admin-user_0
    sudo tljh-config remove-item users.allowed good-user_2

.. _tljh-set-user-limits:

User Server Limits
------------------


* ``limits.memory`` Specifies the maximum memory that can be used by each
  individual user. By default there is no memory limit. The limit can be
  specified as an absolute byte value. You can use
  the suffixes K, M, G or T to mean Kilobyte, Megabyte, Gigabyte or Terabyte
  respectively. Setting it to ``None`` disables memory limits.

  .. code-block:: bash

     sudo tljh-config set limits.memory 4G

  Even if you want individual users to use as much memory as possible,
  it is still good practice to set a memory limit of 80-90% of total
  physical memory. This prevents one user from being able to single
  handedly take down the machine accidentally by OOMing it.

* ``limits.cpu`` A float representing the total CPU-cores each user can use.
  By default there is no CPU limit.
  1 represents one full CPU, 4 represents 4 full CPUs, 0.5 represents
  half of one CPU, etc. This value is ultimately converted to a percentage and
  rounded down to the nearest integer percentage,
  i.e. 1.5 is converted to 150%, 0.125 is converted to 12%, etc.
  Setting it to ``None`` disables CPU limits.

  .. code-block:: bash

     sudo tljh-config set limits.cpu 2

.. _tljh-set-user-env:

User Environment
----------------


    ``user_environment.default_app`` Set default application users are
    launched into. Currently can be set to the following values
    ``jupyterlab`` or ``nteract``

    .. code-block:: bash

       sudo tljh-config set user_environment.default_app jupyterlab

.. _tljh-set-extra-user-groups:

Extra User Groups
=================


``users.extra_user_groups`` is a configuration option that can be used
to automatically add a user to a specific group. By default, there are
no extra groups defined.

Users can be "paired" with the desired, **existing** groups using:

* ``tljh-config set``, if only one user is to be added to the
  desired group:

.. code-block:: bash

  tljh-config set users.extra_user_groups.group1 user1

* ``tljh-config add-item``, if multiple users are to be added to
  the group:

.. code-block:: bash

  tljh-config add-item users.extra_user_groups.group1 user1
  tljh-config add-item users.extra_user_groups.group1 user2


.. _tljh-view-conf:

View current configuration
==========================

To see the current configuration, you can run the following command:

.. code-block:: bash

   sudo tljh-config show

This will print the current configuration of your TLJH. This is very
useful when asking for support!

.. _tljh-reload-hub:


Reloading JupyterHub to apply configuration
===========================================

After modifying the configuration, you need to reload JupyterHub for
it to take effect. You can do so with:

.. code-block:: bash

   sudo tljh-config reload

This should not affect any running users. The JupyterHub will be
restarted and loaded with the new configuration.

.. _tljh-edit-yaml:

Advanced: ``config.yaml``
=========================

``tljh-config`` is a simple program that modifies the contents of the
``config.yaml`` file located at ``/opt/tljh/config/config.yaml``. ``tljh-config``
is the recommended method of editing / viewing configuration since editing
YAML by hand in a terminal text editor is a large source of errors.

To learn more about the ``tljh-config`` usage, you can use the ``--help`` flag.
The ``--help`` flag can be used either directly, to get information about the
general usage of the command or after a positional argument. For example, using
it after an argument like ``remove-item`` gives information about this specific command.

.. code-block:: bash

   sudo tljh-config --help

   usage: tljh-config [-h] [--config-path CONFIG_PATH] {show,set,add-item,remove-item,reload} ...

   positional arguments:
     {show,set,add-item,remove-item,reload}
       show                Show current configuration
       set                 Set a configuration property
       add-item            Add a value to a list for a configuration property
       remove-item         Remove a value from a list for a configuration property
       reload              Reload a component to apply configuration change

   optional arguments:
     -h, --help            show this help message and exit
     --config-path CONFIG_PATH
                           Path to TLJH config.yaml file

.. code-block:: bash

   sudo tljh-config remove-item --help

   usage: tljh-config remove-item [-h] key_path value

   positional arguments:
     key_path    Dot separated path to configuration key to remove value from
     value       Value to remove from key_path

   optional arguments:
     -h, --help  show this help message and exit
