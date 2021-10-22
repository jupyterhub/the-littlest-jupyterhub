.. _topic/env-var-for-tljh-service:

===========================================================
Locale Setting & Other Environment Variables for Jupyterhub
===========================================================

Sometimes you need to run TLJH in the other language environment rather than English.
This will cause some unexpected problems.

e.g.

- The file whose name is not English can not display properly
- Can not open or create the file whose name is not English


 | You may find that no matter what you set in the shell, you will find that the locale is right in the shell only. And in the jupyter notebook/lab which is spawned by TLJH nothing has been changed.

*The reason is that TLJH starts jupyterhub as a systemed service.*

*As a systemed service unit, its environment variables should be set in its config.*


So, we provide a convenient way to set the locale or other environment variables for the service.
We will create a config ``environment_for_system_service.conf`` in the ``/srv/src/tljh`` when the installer is running.
You can add or modify any environment variables in it.

e.g.

.. code-block:: bash

    LANG=zh_CN.UTF-8

**Notice that before you modify the language setting in the conf, install the related fonts and packages first.**



After you do some changes, you should use

.. code-block:: bash

    sudo systemctl daemon-reload

to reload jupyterhub.service`s config.

and

.. code-block:: bash

    sudo tljh-config reload hub

to reload tljh.

**You should be aware that everything set in ``environment_for_system_service.conf`` is only for the ``jupyterhub.service`` .**

It means that you`d better just add the environment variables which the jupyterhub needs instead of all the environment variables in your environment.


