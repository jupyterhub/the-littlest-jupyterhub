.. _howto/share-data:

==========================
Share data with your users
==========================

There are a few options for sharing data with your users, this page covers
a few useful patterns.

Distributing data with `nbgitpuller`
====================================

For small datasets, the simplest way to share data with your users is via
``nbgitpuller`` links. In this case, users click on your link and the dataset
contained in the link's target repository is downloaded to the user's home
directory. Note that a copy of the dataset will be made for each user.

For information on creating and sharing ``nbgitpuller`` links, see
:ref:`tutorials/nbgitpuller`.

Distributing data with a read-only shared folder
================================================

If your data is large or you don't want copies of it to exist, you can create
a read-only shared folder that users have access to. To do this, follow these
steps:

#. Log in to your JupyterHub as an **administrator user**.
#. Create a terminal session within your JupyterHub interface.
#. Create a folder where your data will live:

   .. code-block:: bash

      sudo mkdir /srv/data/mydatafolder

#. Download the data into this folder. For example, using ``sudo curl`` or by running
   a ``python`` script that downloads the data.

#. All users now have read access to the data in this folder.

Optionally, you may also **create a symbolic link to the data folder** in each
**new user's** home directory. To do this, you can use the server's "user skeleton"
directory (``/etc/skel``). Anything that is placed in this directory will also
show up in a new user's home directory. To create a link to the dataset,
follow these steps:

#. Change into the skeleton directory:

   .. code-block:: bash

      cd /etc/skel

#. Create a symbolic link to the data folder

   .. code-block:: bash

      sudo ln -s /src/data/mydatafolder mydatafolder

From now on, when a new user account is created, their home directory will
have this symbolic link (and any other files in ``/etc/skel``) in their home
directory. This will have no effects on the home directories of existing
users.
