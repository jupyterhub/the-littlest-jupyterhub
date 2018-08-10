.. _howto/content/share-data:

==========================
Share data with your users
==========================

There are a few options for sharing data with your users, this page covers
a few useful patterns.

Option 1: Distributing data with `nbgitpuller`
==============================================

For small datasets, the simplest way to share data with your users is via
``nbgitpuller`` links. In this case, users click on your link and the dataset
contained in the link's target repository is downloaded to the user's home
directory. Note that a copy of the dataset will be made for each user.

For information on creating and sharing ``nbgitpuller`` links, see
:ref:`tutorials/nbgitpuller`.

Option 2: Create a read-only shared folder for data
===================================================

If your data is large or you don't want copies of it to exist, you can create
a read-only shared folder that users have access to. To do this, follow these
steps:

#. **Log** in to your JupyterHub as an **administrator user**.

#. **Create a terminal session** with your JupyterHub interface.

   .. image:: ../../images/notebook/new-terminal-button.png
      :alt: New terminal button.
#. **Create a folder** where your data will live. We recommend placing shared
   data in ``/srv``. The following command creates two folders (``/srv/data`` and
   ``/srv/data/my_shared_data_folder``).

   .. code-block:: bash

      sudo -E mkdir -p /srv/data/my_shared_data_folder

#. **Download the data** into this folder. See :ref:`howto/content/add-data` for
   details on how to do this.

#. All users now have read access to the data in this folder.

Add a link to the shared folder in the user home directory
----------------------------------------------------------

Optionally, you may also **create a symbolic link to the shared data folder**
that you created above in each **new user's** home directory.

To do this, you can use the server's **user skeleton directory** (``/etc/skel``).
Anything that is placed in this directory will also
show up in a new user's home directory.

To create a link to the shared folder in the user skeleton directory,
follow these steps:

#. ``cd`` into the skeleton directory:

   .. code-block:: bash

      cd /etc/skel

#. **Create a symbolic link** to the data folder

   .. code-block:: bash

      sudo ln -s /src/data/my_shared_data_folder my_shared_data_folder

#. **Confirm that this worked** by logging in as a new user. You can do this
   by opening a new "incognito" browser window and accessing your JupyterHub.
   After you log in as a **new user**, the folder should appear in your new
   user home directory.

From now on, when a new user account is created, their home directory will
have this symbolic link (and any other files in ``/etc/skel``) in their home
directory. This will have **no effect on the directories of existing
users**.
