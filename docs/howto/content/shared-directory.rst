.. _howto/content/share-data:

=================================================
Shared-directory for users to "publish" Notebooks
=================================================

One way for users to share or "publish" Notebooks in a JupyterHub environment
is to create a shared directory.  Any user can create files in the directory, 
but only the creator may edit that file afterwards.

For instance, in a Hub with three users, User A develops a Notebook in their
`/home` directory.  When it is ready to share, User A copies it to the 
`shared` directory.  At that time, User B and User C can see User A's
Notebook and run it themselves (or view it in a Dashboard layout 
such as `voila` or `panel` if that is running in the Hub), but User B
and User C cannot edit the Notebook.  Only User A can make changes.


#. **Log** in to your JupyterHub as an **administrator user**.

#. **Create a terminal session** with your JupyterHub interface.

   .. image:: ../../images/notebook/new-terminal-button.png
      :alt: New terminal button.
      
#. **Create a folder** where your data will live. We recommend placing shared
   data in ``/srv``.  The following command creates a directory ``/srv/scratch``

   .. code-block:: bash

      sudo mkdir -p /srv/scratch
      
#. **Change group ownership** of the new folder

   .. code-block:: bash
      
      sudo chown  root:jupyterhub-users /srv/scratch
      
#. **Change default permissions to use group**.  The default permissions for new 
   sub-directories uses the global umask (``drwxr-sr-x``), the ``chmod g+s`` tells
   new files to use the default permissions for the group ``jupyterhub-users`` 
   (``rw-r--r--``)
   
   .. code-block:: bash
   
      sudo chmod 777 /srv/scratch
      sudo chmod g+s /srv/scratch
   
   
#. **Create a symbolic link** to the scratch folder in users home directories

   .. code-block:: bash

      sudo ln -s /srv/scratch /etc/skel/scratch
   

