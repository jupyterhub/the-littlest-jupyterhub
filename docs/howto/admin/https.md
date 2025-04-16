(howto-admin-https)=

# Enable HTTPS

Every JupyterHub deployment should enable HTTPS!

HTTPS encrypts traffic so that usernames, passwords and your data are
communicated securely. sensitive bits of information are communicated
securely. The Littlest JupyterHub supports automatically configuring HTTPS
via [Let's Encrypt](https://letsencrypt.org), or setting it up
[manually](#howto-admin-https-manual) with your own TLS key and
certificate. Unless you have a strong reason to use the manual method,
you should use the [Let's Encrypt](#howto-admin-https-letsencrypt)
method.

:::{note}
You _must_ have a domain name set up to point to the IP address on
which TLJH is accessible before you can set up HTTPS.

To do that, you would have to log in to the website of your registrar
and go to the DNS records section. The interface will look like something
similar to this:

```{image} ../../images/dns.png
:alt: Adding an entry to the DNS records
```

:::

(howto-admin-https-letsencrypt)=

## Automatic HTTPS with Let's Encrypt

:::{note}
If the machine you are running on is not reachable from the internet -
for example, if it is a machine internal to your organization that
is cut off from the internet - you can not use this method. Please
set up a DNS entry and HTTPS [manually](#howto-admin-https-manual).
:::

To enable HTTPS via letsencrypt:

```
sudo tljh-config set https.enabled true
sudo tljh-config set https.letsencrypt.email you@example.com
sudo tljh-config add-item https.letsencrypt.domains yourhub.yourdomain.edu
```

where `you@example.com` is your email address and `yourhub.yourdomain.edu`
is the domain where your hub will be running.

Once you have loaded this, your config should look like:

```
sudo tljh-config show
```

```yaml
https:
  enabled: true
  letsencrypt:
    email: you@example.com
    domains:
      - yourhub.yourdomain.edu
```

Finally, you can reload the proxy to load the new configuration:

```
sudo tljh-config reload proxy
```

At this point, the proxy should negotiate with Let's Encrypt to set up a
trusted HTTPS certificate for you. It may take a moment for the proxy to
negotiate with Let's Encrypt to get your certificates, after which you can
access your Hub securely at <https://yourhub.yourdomain.edu>.

These certificates are valid for 3 months. The proxy will automatically
renew them for you before they expire.

(howto-admin-https-manual)=

## Manual HTTPS with existing key and certificate

You may already have an SSL key and certificate for your domain.
If so, you can tell your deployment to use these files:

```
sudo tljh-config set https.enabled true
sudo tljh-config set https.tls.key /etc/mycerts/mydomain.key
sudo tljh-config set https.tls.cert /etc/mycerts/mydomain.cert
```

Once you have loaded this, your config should look like:

```
sudo tljh-config show
```

```yaml
https:
  enabled: true
  tls:
    key: /etc/mycerts/mydomain.key
    cert: /etc/mycerts/mydomain.cert
```

Finally, you can reload the proxy to load the new configuration:

```
sudo tljh-config reload proxy
```

and now access your Hub securely at the domain associated with your certificate.

## Troubleshooting

If you're having trouble with HTTPS, looking at the [traefik proxy logs](troubleshooting-logs-traefik) might help.
