.. _howto/admin/resize:

=================
Resizing a server
=================

As you are using your JupyterHub, you may find that you have a need to increase or decrease 
the amount of resources allocated to your TLJH install. How resources can be reallocated 
will depend on the server interface; consult the installation page for your provider for 
more information. 

However, once resources have been reallocated, you must tell TLJH to make use of these resources,
and verify that the resources have become available.

.. _tljh_verify:

Verifying a Resize 
==================

#. Once you have resized your server, you will need to tell the JupyterHub to make use of 
   these new resources. To accomplish this, you will follow the instructions in 
   :ref:`topic/tljh-config` to edit :ref:`tljh-set-user-limits`, and 
   reload the hub. These steps can be completed using the terminal in the JupyterHub. 
   They can also be completed through the terminal.

#. TLJH configuration options can be verified by viewing the tljh-config output.

   .. code-block:: bash

      sudo tljh-config show


#. If you have changed your memory availability successfully, this will be reflected 
   in the `nbresuse <https://github.com/yuvipanda/nbresuse>`_ extension in the upper-right 
   when you open a Jupyter notebook on the Hub.

   .. image:: ../../images/nbresuse.png
      :alt: nbresuse demonstration

#. If you have changed the number of cores, this can be verified at the command line. 
   ``nproc`` displays the number of available cores, and should be equal to the 
   number of cores you selected in your provider's interface.

   .. code-block:: bash

      nproc --all


#. Disk space changes can be verified, as well. The ``df`` command shows how much disk 
   space is available. The ``-hT`` argument allows us to have this printed in a human readable
   format, and condenses the output to show one storage volume. 

   .. code-block:: bash

      df -hT /home

