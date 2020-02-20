.. _troubleshooting/logs:

===============
Looking at Logs
===============

**Logs** are extremely useful in piecing together what went wrong when things go wrong.
They contain a forensic record of what individual pieces of software were doing
before things went bad, and can help us understand the problem so we can fix it.

TLJH collects logs from JupyterHub, Traefik Proxy, & from each individual
user's notebook server. All the logs are accessible via `journalctl <https://www.freedesktop.org/software/systemd/man/journalctl.html>`_.
The installer also writes logs to disk, to help with cases where the
installer did not succeed.

.. warning::

   If you are providing a snippet from the logs to someone else to help debug
   a problem you might have, be careful to redact any private information (such
   as usernames) from the snippet first!

.. _troubleshooting/logs#installer:

Installer Logs
==============

The JupyterHub installer writes log messages to ``/opt/tljh/installer.log``.
This is very useful if the installation fails for any reason.

.. _troubleshoot_logs_jupyterhub:

JupyterHub Logs
===============

JupyterHub is responsible for user authentication, & starting / stopping user
notebook servers. When there is a general systemic issue with JupyterHub (rather
than a specific issue with a particular user's notebook), looking at the JupyterHub
logs is a great first step.

.. code-block:: bash

   sudo journalctl -u jupyterhub

This command displays logs from JupyterHub itself. See :ref:`journalctl_tips`
for tips on navigating the logs.

.. _troubleshooting/logs/traefik:

Traefik Proxy Logs
==================

`traefik <https://traefik.io/>`_ redirects traffic to JupyterHub / user notebook servers
as necessary & handles HTTPS. Look at this if all you can see in your browser
is one line cryptic error messages, or if you are having trouble with HTTPS.

.. code-block:: bash

   sudo journalctl -u traefik

This command displays logs from Traefik. See :ref:`journalctl_tips`
for tips on navigating the logs.

User Server Logs
================

Each user gets their own notebook server, and this server also produces logs.
Looking at these can be useful when a user can launch their server but run into
problems after that.

.. code-block:: bash

   sudo journalctl -u jupyter-<name-of-user>

This command displays logs from the given user's notebook server. You can get a
list of all users from the "users" button at the top-right of the Admin page.
See :ref:`journalctl_tips` for tips on navigating the logs.

.. _journalctl_tips:

journalctl tips
===============

``journalctl`` has a lot of options to make your life as an administrator
easier. Here are some very basic tips on effective ``journalctl`` usage.

1. When looking at full logs (via ``sudo journalctl -u <some-name>``), the output
   usually does not fit into one screen. Hence, it is *paginated* with
   `less <https://en.wikipedia.org/wiki/Less_(Unix)>`_. This allows you to
   scroll up / down, search for specific words, etc. Some common keyboard shortcuts
   are:

   * Arrow keys to move up / down / left / right
   * ``G`` to navigate to the end of the logs
   * ``g`` to navigate to the start of the logs
   * ``/`` followed by a string to search for & ``enter`` key to search the logs
     from current position on screen to the end of the logs. If there are multiple
     results, you can use ``n`` key to jump to the next search result. Use ``?``
     instead of ``/`` to search backwards from current position
   * ``q`` or ``Ctrl + C`` to exit

   There are plenty of `other commands & options <https://linux.die.net/man/1/less>`_
   to explore if you wish.

2. Add ``-f`` to any ``journalctl`` command to view live logging output
   that updates as new log lines are written. This is extremely useful when
   actively debugging an issue.

   For example, to watch live logs of JupyterHub, you can run:

   .. code-block:: bash

      sudo journalctl -u jupyterhub -f
