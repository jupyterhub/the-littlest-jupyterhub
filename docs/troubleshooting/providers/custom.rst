.. _troubleshooting/providers/custom:

=========================================
Troubleshooting issues on your own server
=========================================

This is an incomplete list of issues people have run into
when installing TLJH on their own servers, and ways they
have fixed them.

Outgoing HTTP proxy required
============================
If your server is behind a firewall that requires a HTTP proxy to reach
the internet, run these commands before running the installer

.. code-block:: bash

    export http_proxy=<your_proxy-server>

HTTPS certificate interception
==============================

If your server is behind a firewall that intercepts HTTPS requests
and re-signs them, you might have to explicitly tell TLJH which
certificates to use.

.. code::

    export REQUESTS_CA_BUNDLE=</directory/with/your/ssl/certificates>
    sudo npm config set cafile=</directory/with/your/ssl/certificates>