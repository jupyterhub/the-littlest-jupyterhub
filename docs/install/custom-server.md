(install-custom)=

# Installing on your own server

Follow this guide if your cloud provider doesn't have a direct tutorial, or
you are setting this up on a bare metal server.

:::{warning}
Do **not** install TLJH directly on your laptop or personal computer!
It will most likely open up exploitable security holes when run directly
on your personal computer.
:::

:::{note}
Running TLJH _inside_ a docker container is not supported, since we depend
on systemd. If you want to run TLJH locally for development, see
[](/contributing/dev-setup).
:::

## Goal

By the end of this tutorial, you should have a JupyterHub with some admin
users and a user environment with packages you want installed running on
a server you have access to.

## Pre-requisites

1. Some familiarity with the command line.
2. A server running Ubuntu 20.04+ where you have root access (Ubuntu 22.04 LTS recommended).
3. At least **1GB** of RAM on your server.
4. Ability to `ssh` into the server & run commands from the prompt.
5. An **IP address** where the server can be reached from the browsers of your target audience.

If you run into issues, look at the specific [troubleshooting guide](/troubleshooting/providers/custom)
for custom server installations.

## Step 1: Installing The Littlest JupyterHub

1. Using a terminal program, SSH into your server. This should give you a prompt where you can
   type commands.

2. Make sure you have `python3`, `python3-dev`, `curl` and `git` installed.

   ```
   sudo apt install python3 python3-dev git curl
   ```

3. Copy the text below, and paste it into the terminal. Replace
   `<admin-user-name>` with the name of the first **admin user** for this
   JupyterHub. Choose any name you like (don't forget to remove the brackets!).
   This admin user can log in after the JupyterHub is set up, and
   can configure it to their needs. **Remember to add your username**!

   ```bash
   curl -L https://tljh.jupyter.org/bootstrap.py | sudo -E python3 - --admin <admin-user-name>
   ```

   :::{note}
   See [](/topic/installer-actions) if you want to understand exactly what the installer is doing.
   [](/topic/customizing-installer) documents other options that can be passed to the installer.
   :::

4. Press `Enter` to start the installation process. This will take 5-10 minutes,
   and will say `Done!` when the installation process is complete.

5. Copy the **Public IP** of your server, and try accessing `http://<public-ip>` from
   your browser. If everything went well, this should give you a JupyterHub login page.

   ```{image} ../images/first-login.png
   :alt: JupyterHub log-in page
   ```

6. Login using the **admin user name** you used in step 3. You can choose any
   password that you wish. Use a
   strong password & note it down somewhere, since this will be the password for
   the admin user account from now on.

7. Congratulations, you have a running working JupyterHub!

## Step 2: Adding more users

```{eval-rst}
.. include:: add_users.txt
```

## Step 3: Install conda / pip packages for all users

```{eval-rst}
.. include:: add_packages.txt
```

## Step 4: Setup HTTPS

Once you are ready to run your server for real, and have a domain, it's a good
idea to proceed directly to [](/howto/admin/https).
