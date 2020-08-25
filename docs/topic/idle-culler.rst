.. _topic/idle-culler:

=============================
Culling idle notebook servers
=============================

The idle culler automatically shuts down user notebook servers when they have
not been used for a certain time period, in order to reduce the total resource
usage on your JupyterHub.

JupyterHub pings the user's notebook server at certain time intervals. If no response
is received from the server during this checks and the timeout expires, the server is
considered to be *inactive (idle)* and will be culled.

The `idle culler <https://github.com/jupyterhub/jupyterhub-idle-culler>`_ is a JupyterHub service that is installed and enabled by default in TLJH.
It can be configured using tljh-config. For advanced use-cases, like purging old user data,
the idle culler configuration can be extended beyond tljh-config options, using custom 
`jupyterhub_config.py snippets <https://tljh.jupyter.org/en/latest/topic/escape-hatch.html?highlight=escape-hatch#extending-jupyterhub-config-py>`__.


Default settings
================

By default, JupyterHub will ping the user notebook servers every 60s to check their
status. Every server found to be idle for more than 10 minutes will be culled.

.. code-block:: python

	services.cull.every = 60
	services.cull.timeout = 600

Because the servers don't have a maximum age set, an active server will not be shut down
regardless of how long it has been up and running.

.. code-block:: python

	services.cull.max_age = 0

If after the culling process, there are users with no active notebook servers, by default,
the users will not be culled alongside their notebooks and will continue to exist.

.. code-block:: python

	services.cull.users = False


Configuring the idle culler
===========================

The available configuration options are:

Idle timeout
------------
The idle timeout is the maximum time (in seconds) a server can be inactive before it
will be culled. The timeout can be configured using:

.. code-block:: bash

	sudo tljh-config set services.cull.timeout <max-idle-sec-before-server-is-culled>
	sudo tljh-config reload

Idle check interval
-------------------
The idle check interval represents how frequent (in seconds) the Hub will
check if there are any idle servers to cull. It can be configured using:

.. code-block:: bash

 	sudo tljh-config set services.cull.every <number-of-sec-this-check-is-done>
 	sudo tljh-config reload

Maximum age
-----------
The maximum age sets the time (in seconds) a server should be running.
The servers that exceed the maximum age, will be culled even if they are active.
A maximum age of 0, will deactivate this option.
The maximum age can be configured using:

.. code-block:: bash

 	sudo tljh-config set services.cull.max_age <server-max-age>
 	sudo tljh-config reload

User culling
------------
In addition to servers, it is also possible to cull the users. This is usually
suited for temporary-user cases such as *tmpnb*.
User culling can be activated using the following command:

.. code-block:: bash

 	sudo tljh-config set services.cull.users True
 	sudo tljh-config reload

Concurrency
-----------
Deleting a lot of users at the same time can slow down the Hub.
The number of concurrent requests made to the Hub can be configured using:

.. code-block:: bash

 	sudo tljh-config set services.cull.concurrency <number-of-concurrent-hub-requests>
 	sudo tljh-config reload

Because TLJH it's used for a small number of users, the cases that may require to
modify the concurrency limit should be rare.


Disabling the idle culler
=========================

The idle culling service is enabled by default. To disable it, use the following
command:

.. code-block:: bash

   sudo tljh-config set services.cull.enabled False
   sudo tljh-config reload
