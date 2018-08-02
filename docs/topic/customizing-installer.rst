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
