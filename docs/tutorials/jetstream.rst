.. _tutorial_quickstart_jetstream:

Tutorial: JupyterHub on Jetstream
=================================

Goal
----

By the end of this tutorial, you should have a JupyterHub with some admin
users and a user environment with packages you want installed running on
`Jetstream <https://jetstream-cloud.org/>`_.

Prerequisites
-------------

#. A Jetstream account with an XSEDE allocation; for more information, `go to the Jetstream Allocations help page <http://wiki.jetstream-cloud.org/Jetstream+Allocations>`__.
#. Some familiarity with the command line.

Step 1: Installing The Littlest JupyterHub
------------------------------------------

Let's create the server on which we can run JupyterHub.

#. Log in to `the Jetstream portal <https://use.jetstream-cloud.org/>`_. You need an allocation
   to launch instances.

#. Select the **Launch New Instance** option to get going.

   .. image:: ../images/providers/jetstream/launch-instance-first-button.png
      :alt: Launch new instance button with description.

   This takes you to a page with a list of base images you can choose for your
   server.

#. Under **Image Search**, search for **Ubuntu 18.04**, and select the
   **Ubuntu 18.04 Devel and Docker** image.

   .. image:: ../images/providers/jetstream/select-image.png
      :alt: Select Ubuntu 18.04 x64 image from image list

#. Once selected, you will see more information about this image. Click the
   **Launch** button on the top right.

   .. image:: ../images/providers/jetstream/launch-instance-second-button.png
      :alt: Launch selected image with Launch button on top right

#. A dialog titled **Launch an Instance / Basic Options** pops up, with various
   options for configuring your instance.

   .. image:: ../images/providers/jetstream/launch-instance-dialog.png
      :alt: Launch an Instance / Basic Options dialog box

   #. Give your server a descriptive **Instance Name**.
   #. Select an appropriate **Instance Size**. We suggest m1.medium or larger.
   #. If you have multiple allocations, make sure you are 'charging' this server
      to the correct allocation.

#. Click the **Advanced Options** link in the bottom left of the popup. This
   lets us configure what the server should do when it starts up. We will use
   this to install The Littlest JupyterHub.

   A dialog titled **Launch an Instance / Advanced Options** should pop up.

   .. image:: ../images/providers/jetstream/add-deployment-script-dialog.png
      :alt: Dialog box allowing you to add a new script.

#. Click the **Create New Script** button. This will open up another dialog
   box!

   .. image:: ../images/providers/jetstream/create-script-dialog.png
      :alt: Launch an Instance / Advanced Options dialog box

#. Under **Input Type**, select **Raw Text**. This should make a text box titled
   **Raw Text** visible on the right side of the dialog box.
   Copy the text below, and paste it into the **Raw Text** text box. Replace
   ``<admin-user-name>`` with the name of the first **admin user** for this
   JupyterHub. This admin user can log in after the JupyterHub is set up, and
   can configure it to their needs. Remember the username!

   .. code-block:: bash

    #!/bin/bash
    curl https://raw.githubusercontent.com/yuvipanda/the-littlest-jupyterhub/master/bootstrap/bootstrap.py \
     | sudo python3 - \
       --admin <admin-user-name>

#. Under **Execution Strategy Type**, select **Run script on first boot**.

#. Under **Deployment Type**, select **Wait for script to complete**.

#. Click the **Save and Add Script** button on the bottom right. This should hide
   the dialog box.

#. Click the **Continue to Launch** button on the bottom right. This should put you
   back in the **Launch an Instance / Basic Options** dialog box again.

#. Click the **Launch Instance** button on the bottom right. This should turn it
   into a spinner, and your server is getting created!

   .. image:: ../images/providers/jetstream/launching-spinner.png
      :alt: Launch button turns into a spinner

#. You'll now be shown a dashboard with all your servers and their states. The
   server you just launched will progress through various stages of set up,
   and you can see the progress here.

   .. image:: ../images/providers/jetstream/deployment-in-progress.png
      :alt: Instances dashboard showing deployment in progress.

#. It will take about ten minutes for your server to come up. The status will
   say **Active** and the progress bar will be a solid green. At this point,
   your JupyterHub is ready for use!

#. Copy the **IP Address** of your server, and try accessing it from a web
   browser. It should give you a JupyterHub login page.

   .. image:: ../images/first-login.png
      :alt: JupyterHub log-in page

#. Login using the **admin user name** you used in step 8, and a password. Use a
   strong password & note it down somewhere, since this will be the password for
   the admin user account from now on.

#. Congratulations, you have a running working JupyterHub!

Step 2: Adding more users
-------------------------

Most administration & configuration of the JupyterHub can be done from the
web UI directly. Let's add a few users who can log in!

#. Open the **Control Panel** by clicking the control panel button on the top
   right of your JupyterHub.

   .. image:: ../images/control-panel-button.png
      :alt: Control panel button in notebook, top right

#. In the control panel, open the **Admin** link in the top left.

   .. image:: ../images/admin/admin-access-button.png
      :alt: Admin button in control panel, top left

   This opens up the JupyterHub admin page, where you can add / delete users,
   start / stop peoples' servers and see who is online.

#. Click the **Add Users** button.

   .. image:: ../images/admin/add-users-button.png
      :alt: Add Users button in the admin page

   A **Add Users** dialog box opens up.

#. Type the names of users you want to add to this JupyterHub in the dialog box,
   one per line.

   .. image:: ../images/admin/add-users-dialog.png
      :alt: Adding users with add users dialog

   You can tick the **Admin** checkbox if you want to give admin rights to all
   these users too.

#. Click the **Add Users** button in the dialog box. Your users are now added
   to the JupyterHub! When they log in for the first time, they can set their
   password - and use it to log in again in the future.

   **Note**: These users will be added as UNIX users on the underlying
   Jetstream instance, too, and admin users will have ``sudo`` privileges.
   (The user will be created the first time the user's server is started,
   e.g. upon first login.)

Congratulations, you now have a multi user JupyterHub that you can add arbitrary
users to!

Step 3: Install conda / pip packages for all users
--------------------------------------------------

The **User Environment** is a conda environment that is shared by all users
in the JupyterHub. Libraries installed in this environment are immediately
available to all users. Admin users can install packages in this environment
with ``sudo -E``.

#. Log in as an admin user and open a Terminal in your Jupyter Notebook.

   .. image:: ../images/notebook/new-terminal-button.png
      :alt: New Terminal button under New menu

#. For example, try installing `gdal <https://anaconda.org/conda-forge/gdal>`_ from `conda-forge <https://conda-forge.org/>`_.

   .. code-block:: bash

      sudo -E conda install -y -c conda-forge gdal

   The ``sudo -E`` is very important!

#. Alternatively, try installing `there <https://pypi.org/project/there/>`_ with ``pip``.

   .. code-block:: bash

      sudo -E pip install there

The packages ``gdal`` and ``there`` are now available to all users in JupyterHub.
If a user already had a python notebook running, they need to restart their notebook's
kernel to make the new libraries available.

See :ref:`user_environment` for more information.
