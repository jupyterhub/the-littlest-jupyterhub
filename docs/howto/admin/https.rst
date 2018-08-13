.. _howto/admin/https:

============
Enable HTTPS
============

Every JupyterHub deployment should enable HTTPS!
HTTPS encrypts traffic so that usernames and passwords and other potentially sensitive bits of information are communicated securely.
The Littlest JupyterHub supports automatically configuring HTTPS via `Let's Encrypt <https://letsencrypt.org>`_,
or setting it up :ref:`manually <manual_https>` with your own TLS key and certificate.
If you don't know how to do that,
then :ref:`Let's Encrypt <letsencrypt>` is probably the right path for you.


.. _letsencrypt:

Automatic HTTPS with Let's Encrypt
==================================

To enable HTTPS via letsencrypt::

    sudo tljh-config set https.enabled true
    sudo tljh-config set https.letsencrypt.email you@example.com
    sudo tljh-config add-item https.letsencrypt.domains yourhub.yourdomain.edu

where ``you@example.com`` is your email address and ``yourhub.yourdomain.edu`` is the domain where your hub will be running.

Once you have loaded this, your config should look like::

    sudo tljh-config show


.. sourcecode:: yaml

    https:
      enabled: true
      letsencrypt:
        email: you@example.com
        domains:
        - yourhub.yourdomain.edu

Finally, you can reload the proxy to load the new configuration::

    sudo tljh-config reload proxy

At this point, the proxy should negotiate with Let's Encrypt to set up a trusted HTTPS certificate for you.
It may take a moment for the proxy to negotiate with Let's Encrypt to get your certificates, after which you can access your Hub securely at https://yourhub.yourdomain.edu.

.. _manual_https:

Manual HTTPS with existing key and certificate
==============================================

You may already have an SSL key and certificate.
If so, you can tell your deployment to use these files::

    sudo tljh-config set https.enabled true
    sudo tljh-config set https.tls.key /etc/mycerts/mydomain.key
    sudo tljh-config set https.tls.cert /etc/mycerts/mydomain.cert


Once you have loaded this, your config should look like::

    sudo tljh-config show


.. sourcecode:: yaml

    https:
      enabled: true
      tls:
        key: /etc/mycerts/mydomain.key
        cert: /etc/mycerts/mydomain.cert

Finally, you can reload the proxy to load the new configuration::

    sudo tljh-config reload proxy

and now access your Hub securely at https://yourhub.yourdomain.edu.
