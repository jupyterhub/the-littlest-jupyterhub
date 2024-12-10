(install-jetstream)=

# Installing on Jetstream

## Goal

By the end of this tutorial, you should have a JupyterHub with some admin
users and a user environment with packages you want installed running on
[Jetstream](https://jetstream-cloud.org/).

## Prerequisites

1. A Jetstream account with an ACCESS allocation; for more information,
   see the [Jetstream Allocations help page](https://docs.jetstream-cloud.org/alloc/overview/).

## Step 1: Installing The Littlest JupyterHub

Let's create the server on which we can run JupyterHub.

1.  Log in to [the Jetstream portal](https://use.jetstream-cloud.org/). You need an allocation
    to launch instances.

2.  Select the **Create** option, and then **Instance** to get going.

    ```{image} ../images/providers/jetstream/launch-instance-first-button.png
    :alt: Create new instance button.
    ```

    This takes you to a page with a list of base images you can choose for your
    server.

3.  Under **Choose an Instance Source**, select **Ubuntu 24.04 (latest)** image.

    ```{image} ../images/providers/jetstream/select-image.png
    :alt: Select Ubuntu 24.04 (latest) from image list
    ```

4.  A page titled **Create Instance** loads, with various
    options for configuring your instance.

    ```{image} ../images/providers/jetstream/launch-instance-dialog.png
    :alt: Launch an Instance / Basic Options dialog box
    ```

    1. Give your server a descriptive **Name**.

    2. Select an appropriate **Flavor**. We suggest m3.medium or larger.
       You can resize your instance later if you need.

       Check out our guide on How To [](/howto/admin/resource-estimation) to help pick
       how much Memory, CPU & disk space your server needs.

5.  Click the **Advanced Options** link in the bottom left of the popup. This
    lets us configure what the server should do when it starts up. We will use
    this to install The Littlest JupyterHub.

    A dialog titled **Launch an Instance / Advanced Options** should pop up.

    ```{image} ../images/providers/jetstream/add-deployment-script-dialog.png
    :alt: Dialog box allowing you to add a new script.
    ```

6.  Click the **Create New Script** button. This will open up another dialog
    box!

    ```{image} ../images/providers/jetstream/create-script-dialog.png
    :alt: Launch an Instance / Advanced Options dialog box
    ```

7.  Under **Input Type**, select **Raw Text**. This should make a text box titled
    **Raw Text** visible on the right side of the dialog box.
    Copy the text below, and paste it into the **Raw Text** text box. Replace
    `<admin-user-name>` with the name of the first **admin user** for this
    JupyterHub. This admin user can log in after the JupyterHub is set up, and
    can configure it to their needs. **Remember to add your username**!

    ```bash
    #!/bin/bash
    curl -L https://tljh.jupyter.org/bootstrap.py \
      | sudo python3 - \
        --admin <admin-user-name>
    ```

    :::{note}
    See [](/topic/installer-actions) if you want to understand exactly what the installer is doing.
    [](/topic/customizing-installer) documents other options that can be passed to the installer.
    :::

8.  Under **Execution Strategy Type**, select **Run script on first boot**.

9.  Under **Deployment Type**, select **Wait for script to complete**.

10. Click the **Save and Add Script** button on the bottom right. This should hide
    the dialog box.

11. Click the **Continue to Launch** button on the bottom right. This should put you
    back in the **Launch an Instance / Basic Options** dialog box again.

12. Click the **Launch Instance** button on the bottom right. This should turn it
    into a spinner, and your server is getting created!

    ```{image} ../images/providers/jetstream/launching-spinner.png
    :alt: Launch button turns into a spinner
    ```

13. You'll now be shown a dashboard with all your servers and their states. The
    server you just launched will progress through various stages of set up,
    and you can see the progress here.

    ```{image} ../images/providers/jetstream/deployment-in-progress.png
    :alt: Instances dashboard showing deployment in progress.
    ```

14. It will take about ten minutes for your server to come up. The status will
    say **Active** and the progress bar will be a solid green. At this point,
    your JupyterHub is ready for use!

15. Copy the **IP Address** of your server, and try accessing it from a web
    browser. It should give you a JupyterHub login page.

    ```{image} ../images/first-login.png
    :alt: JupyterHub log-in page
    ```

16. Login using the **admin user name** you used in step 8, and a password. Use a
    strong password & note it down somewhere, since this will be the password for
    the admin user account from now on.

17. Congratulations, you have a running working JupyterHub!

## Step 2: Adding more users

```{include} add-users.md

```

## Step 3: Install conda / pip packages for all users

```{include} add-packages.md

```
