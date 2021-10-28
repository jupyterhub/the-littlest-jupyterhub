.. _howto/providers/digitalocean:

================================================
Perform common Digital Ocean configuration tasks
================================================

This page lists various common tasks you can perform on your
Digital Ocean virtual machine.

.. _howto/providers/digitalocean/resize:

Resizing your droplet
=====================

As you use your JupyterHub, you may find that you need more memory, 
disk space, or CPUs. Digital Ocean servers can be resized in the 
"Resize Droplet" panel. These instructions take you through the process.

#. First, click on the name of your newly-created
   Droplet to enter its configuration page.

#. Next, **turn off your Droplet**. This allows DigitalOcean to make
   modifications to your VM. This will shut down your JupyterHub (temporarily).

   .. image:: ../../images/providers/digitalocean/power-off.png
      :alt: Power off your Droplet
      :width: 200px

#. Once your Droplet has been turned off, click "Resize",
   which will take you to a menu with options to resize your VM.

   .. image:: ../../images/providers/digitalocean/resize-droplet.png
      :alt: Resize panel of digital ocean

#. Decide what kinds of resources you'd like to resize, then click on a new VM
   type in the list below. Finally, click "Resize". This may take a few moments!

#. Once your Droplet is resized, **turn your Droplet back on**. This makes your JupyterHub
   available to the world once again. This will take a few moments to complete.

Now that you've resized your Droplet, you may want to change the resources available
to your users. Further information on making more resources available to
users and verifying resource availability can be found in :ref:`howto/admin/resize`. 
