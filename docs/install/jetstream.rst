.. _install/jetstream:

=======================
Installing on Jetstream
=======================

Goal
====

By the end of this tutorial, you should have a JupyterHub with some admin
users and a user environment with packages you want installed running on
`Jetstream <https://jetstream-cloud.org/>`_.

Prerequisites
=============

#. A Jetstream account with an XSEDE allocation; for more information,
   see the `Jetstream Allocations help page <http://wiki.jetstream-cloud.org/Jetstream+Allocations>`_.

Step 1: Installing The Littlest JupyterHub
==========================================

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
      Make sure your instance has at least **1GB** of RAM.

      Check out our guide on How To :ref:`howto/admin/resource-estimation` to help pick
      how much Memory, CPU & disk space your server needs.

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
   can configure it to their needs. **Remember to add your username**!

   .. code-block:: bash

      #!/bin/bash
      curl -L https://tljh.jupyter.org/bootstrap.py \
        | sudo python3 - \
          --admin <admin-user-name>

   .. note::

      See :ref:`topic/installer-actions` if you want to understand exactly what the installer is doing.
      :ref:`topic/customizing-installer` documents other options that can be passed to the installer.

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
==========================

.. include:: add_users.txt

Step 3: Install conda / pip packages for all users
==================================================

.. include:: add_packages.txt
