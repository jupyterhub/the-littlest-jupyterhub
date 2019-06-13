.. _topic/idle-culler:

=============================
Culling idle notebook servers
=============================

The idle culler is a hub-managed service that automatically shuts down idle
single-user notebook servers in order to free up resources. After culling, any
in-memory data will be lost.


Disabling the idle culler
=========================

The idle culling service is enabled by default. To disable it, use the following
command:

.. code-block:: bash

   sudo tljh-config set services.cull.enabled False


Configuring the idle culler
===========================

By **default**,  JupyterHub will:
	* Run the culling process every minute.
	* Cull any user servers that have been inactive for more than 10 minutes.

The configuration options available are:

Idle timeout
------------

The idle timeout (in seconds) can be configured using:

.. code-block:: bash

	sudo tljh-config set services.cull.timeout <max-idle-sec-before-server-is-culled>

*By default services.cull.timeout = 600*

Idle check interval
-------------------

The interval (in seconds) for checking for idle servers to cull can be configured using:

.. code-block:: bash

 	sudo tljh-config set services.cull.every <number-of-sec-this-check-is-done>

*By default services.cull.every = 60*

Maximum age
-----------

The maximum age (in seconds) of servers that should be culled even if they are active
can be configured using:

.. code-block:: bash

 	sudo tljh-config set services.cull.max_age <server-max-age>

*By default services.cull.max_age = 0*

User culling
------------

In addition to servers, the users will also be culled if the following command is used:

.. code-block:: bash

 	sudo tljh-config set services.cull.users True

*By default services.cull.users = False*

Concurrency
-----------

The number of concurrent requests made to the Hub ca be configured using:

.. code-block:: bash

 	sudo tljh-config set services.cull.concurrency <number-of-concurrent-hub-requests>

*By default services.cull.concurrency = 5*
