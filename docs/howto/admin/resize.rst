.. _howto/admin/resize:

=================================================
Resize the resources available to your JupyterHub
=================================================

As you are using your JupyterHub, you may need to increase or decrease
the amount of resources allocated to your TLJH install. The kinds of resources that can be
allocated, as well as the process to do so, will depend on the provider / interface for your
VM. We recommend consulting the installation page for your provider for more information. This
page covers the steps your should take on your JupyterHub *after* you've reallocated resources on
the cloud provider of your choice.

Currently there are instructions to resize your resources on the following providers:

* :ref:`Digital Ocean <howto/providers/digitalocean/resize>`.

Once resources have been reallocated, you must tell TLJH to make use of these resources,
and verify that the resources have become available.

Verifying a Resize
==================

#. Once you have resized your server, tell the JupyterHub to make use of
   these new resources. To accomplish this, follow the instructions in
   :ref:`topic/tljh-config` to set new memory or CPU limits and reload the hub. This can be completed
   using the terminal in the JupyterHub (or via SSH-ing into your VM and using this terminal).

#. TLJH configuration options can be verified by viewing the tljh-config output.

   .. code-block:: bash

      sudo tljh-config show

   Double-check that your changes are reflected in the output.

#. **To verify changes to memory**, confirm that it worked by starting
   a new server (if you had one previously running, click "Control Panel -> Stop My Server" to
   shut down your active server first), opening a notebook, and checking the value of the
   `jupyter-resource-usage <https://github.com/jupyter-server/jupyter-resource-usage>`_ extension in the upper-right.

   .. image:: ../../images/nbresuse.png
      :alt: jupyter-resource-usage demonstration

#. **To verify changes to CPU**, use the ``nproc`` from a terminal.
   This command displays the number of available cores, and should be equal to the
   number of cores you selected in your provider's interface.

   .. code-block:: bash

      nproc --all

#. **To verify currently-available disk space**, use the ``df`` command in a terminal. This shows
   how much disk space is available. The ``-hT`` argument allows us to have this printed in a human readable
   format, and condenses the output to show one storage volume. Note that currently you cannot
   change the disk space on a per-user basis.

   .. code-block:: bash

      df -hT /home
