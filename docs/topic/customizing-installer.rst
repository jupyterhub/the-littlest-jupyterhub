.. _topic/customizing-installer:

=========================
Customizing the Installer
=========================

The installer can be customized with commandline parameters. The default installer
is executed as:

.. code-block:: bash

    curl https://raw.githubusercontent.com/jupyterhub/the-littlest-jupyterhub/master/bootstrap/bootstrap.py \
     | sudo python3 - \
       <parameters>

This page documents the various options you can pass as commandline parameters to the installer.

.. _topic/customizing-installer/admin:

Adding admin users
===================

``--admin <username>`` adds user ``<username>`` to JupyterHub as an admin user.
This can be repeated multiple times.

For example, to add ``admin-user1`` and ``admin-user2`` as admins when installing, you
would do:

.. code-block:: bash

    curl https://raw.githubusercontent.com/jupyterhub/the-littlest-jupyterhub/master/bootstrap/bootstrap.py \
     | sudo python3 - \
       --admin admin-user1 --admin admin-user2

Installing python packages in the user environment
==================================================

``--user-requirements-txt-url <url-to-requirements.txt>`` installs packages specified
in the ``requirements.txt`` located at the given URL into the user environment at install
time. This is very useful when you want to set up a hub with a particular user environment
in one go.

For example, to install the latest requirements to run UC Berkeley's data8 course
in your new hub, you would run:

.. code-block:: bash

    curl https://raw.githubusercontent.com/jupyterhub/the-littlest-jupyterhub/master/bootstrap/bootstrap.py \
     | sudo python3 - \
       --user-requirements-txt-url https://raw.githubusercontent.com/data-8/materials-sp18/master/requirements.txt

The URL **must** point to a working requirements.txt. If there are any errors, the installation
will fail.

.. note::

   When pointing to a file on GitHub, make sure to use the 'Raw' version. It should point to
   ``raw.githubusercontent.com``, not ``github.com``.

Installing TLJH plugins
=======================

The Littlest JupyterHub can install additional *plugins* that provide additional
features. They are most commonly used to install a particular *stack* - such as
the `PANGEO Stack <https://github.com/yuvipanda/tljh-pangeo>`_ for earth sciences
research, a stack for a praticular class, etc.

``--plugin <plugin-to-install>`` installs and activates a plugin. You can pass it
however many times you want. Since plugins are distributed as python packages,
``<plugin-to-install>`` can be anything that can be passed to ``pip install`` -
``plugin-name-on-pypi==<version>`` and ``git+https://github.com/user/repo@tag``
are the most popular ones. Specifying a version or tag is highly recommended.

For example, to install the PANGEO Plugin version 0.1 in your new TLJH install,
you would use:

.. code-block:: bash

   curl https://raw.githubusercontent.com/jupyterhub/the-littlest-jupyterhub/master/bootstrap/bootstrap.py \
    | sudo python3 - \
      --plugin git+https://github.com/yuvipanda/tljh-pangeo@v0.1


.. note::

   Plugins are extremely powerful and can do a large number of arbitrary things.
   Only install plugins you trust.
