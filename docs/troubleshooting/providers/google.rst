======================================
Troubleshooting issues on Google Cloud
======================================

This is an incomplete list of issues people have run into when running
TLJH on Google Cloud, and how they have fixed them!

'Connection Refused' error after restarting server
==================================================

If you restarted your server from the Google Cloud console & then try to access
your JupyterHub from a browser, you might get a **Connection Refused** error.
This is most likely because the **External IP** of your server has changed.

Check the **External IP** in the `Google Cloud Console -> Compute Engine -> VM instances
<https://console.cloud.google.com/compute/instances>`_ screen
matches the IP you are trying to access. If you have a domain name pointing to the
IP address, you might have to change it to point to the new correct IP.

You can prevent External IP changes by `reserving the static IP
<https://cloud.google.com/compute/docs/ip-addresses/reserve-static-external-ip-address#promote_ephemeral_ip>`_
your server is using.
