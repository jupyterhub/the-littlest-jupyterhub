Frequently Asked Questions
==========================

I stopped and started my VM, and now JupyterHub doesn't work!
----------------------------------------------------------------------

Depending on the VM provider that you're using, stopping your VM might
cause a new External IP address to be generated. If this happens, then your
old IP address will no longer work.

Figure out what the new External IP address is, then SSH into it and
restart your JupyterHub with::

    sudo systemctl restart jupyterhub

And the new External IP should now start working.
