# Troubleshooting issues on Google Cloud

This is an incomplete list of issues people have run into when running
TLJH on Google Cloud, and how they have fixed them!

## Viewing VM instance logs

In addition to [installer, JupyterHub, traefik, and other logs](#troubleshooting-logs)
you can view VM instance logs on Google Cloud to help diagnose issues. These logs will contain
detailed information and error stack traces and can be viewed from
[Google Cloud Console -> Compute Engine -> VM instances](https://console.cloud.google.com/compute/instances).
Once you select your TLJH instance, select **Serial port 1 (console)**:

```{image} ../../images/providers/google/serial-port-console.png
:alt: Serial port 1 (console) under Logs heading
```

:::{tip}
The console will show the logs of any startup scripts you configured for your instance,
making it easy to see if it has completed and/or encountered any errors.
:::

## 'Connection Refused' error after restarting server

If you restarted your server from the Google Cloud console & then try to access
your JupyterHub from a browser, you might get a **Connection Refused** error.
This is most likely because the **External IP** of your server has changed.

Check the **External IP** in the [Google Cloud Console -> Compute Engine -> VM instances](https://console.cloud.google.com/compute/instances) screen
matches the IP you are trying to access. If you have a domain name pointing to the
IP address, you might have to change it to point to the new correct IP.

You can prevent External IP changes by [reserving the static IP](https://cloud.google.com/compute/docs/ip-addresses/reserve-static-external-ip-address#promote_ephemeral_ip)
your server is using.

## Issues caused by lack of disk space

If your boot disk becomes full, this can cause your instance to become unavailable,
among other problems. If your instance appears up and running in the console but
you cannot access it at your configured external IP/domain name, this could be caused
by a lack of disk space.

You can explore your [VM logs in the console](#viewing-vm-instance-logs) to determine
if any issues you are experiencing indicate disk space issues.

To resolve these types of issues, you can
[increase your boot disk size](#howto-providers-google-resize-disk).
