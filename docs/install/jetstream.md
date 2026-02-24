(install-jetstream)=

# Installing on Jetstream2

## Goal

By the end of this tutorial, you should have a JupyterHub with some admin
users and a user environment with packages you want installed running on
[Jetstream2](https://jetstream-cloud.org/).

## Prerequisites

1. An ACCESS ID, and membership in an allocation with access to Jetstream2 resources; for more information,
   see the [Jetstream2 Allocations Overview page](https://docs.jetstream-cloud.org/alloc/overview/) and the [Get started with Jetstream2 guide](https://jetstream-cloud.org/get-started/).

## Step 1: Launch a Jetstream2 instance

We'll create a new Jetstream2 instance:

1.  Log in to the [Jetstream2 portal](https://use.jetstream-cloud.org/). You must have (and select) an allocation in order to launch instances. Click the allocation you want to charge.
2.  Click **Create** ➜ **Instance**.
3.  From the list of images, select **Ubuntu 24.04** (Ubuntu 22.04/Jammy or newer is supported).
4.  In the **Create Instance** dialog:
    1. Set a descriptive **Instance Name** (this is used in the default hostname and helps users recognize it).
    2. Choose an **Instance Size**. We suggest `m3.small` (2 vCPUs / 6 GiB RAM) or larger for more than a couple of users. The absolute minimum TLJH can start with is about **1 GiB** RAM, but you'll quickly run out with real workloads.
       - See the resource estimation guide: [Choosing resources](/howto/admin/resource-estimation) for help picking CPU, RAM, and disk.
    3. (Optional) Increase the **Volume Size** if you expect many users or large datasets. You can not easily shrink later.
5.  Launch the instance (click **Create** button at the bottom of the form).

## Step 2: Install The Littlest JupyterHub

1. Wait a few minutes for the instance to show the status "Ready"
2. Copy the **Hostname** under **Credentials**. It will look like `yourinstancename.<allocation-id>.projects.jetstream-cloud.org`. Keep it handy, we will use it multiple times in the next steps.

3. SSH into the instance with the `exouser` user:

   ```bash
   ssh exouser@yourinstancename.<allocation-id>.projects.jetstream-cloud.org
   ```

   Need the passphrase? In Exosphere, open **Instances**, select your
   JupyterHub instance, and expand **Credentials**. Click **Show Passphrase**
   next to the `exouser` entry to reveal or copy it before running the
   `ssh` command.

4. Run the TLJH bootstrap script. Replace `<admin-user-name>` with the Linux username you want to use for the first JupyterHub admin account (for example, your GitHub username). Do not include `<` or `>` in the command. This user will be able to log in after setup and administer the hub.

   ```bash
   curl -L https://tljh.jupyter.org/bootstrap.py | sudo -E python3 - --admin <admin-user-name>
   ```

   Optional quick sanity check:

   ```bash
   sudo systemctl is-active jupyterhub traefik
   ```

5. Open the Hostname in a web browser (http on port 80). You should see the JupyterHub login page (typically titled `JupyterHub` with a `Sign in` button). Your browser will warn about the site not being secure (no HTTPS)—we'll enable HTTPS in the next step. Do not log in yet; first set up HTTPS, so we avoid transmitting the password in clear text.

## Step 3: Enable HTTPS

Encrypted (HTTPS) access is strongly recommended before inviting users.

See the full guide: [Enable HTTPS](/howto/admin/https). Below is a quick recipe for using the default Jetstream-provided hostname.

1. In the terminal inside the instance, configure Let's Encrypt (replace with a real email you control, and the correct hostname):
   ```bash
   sudo tljh-config set https.enabled true
   sudo tljh-config set https.letsencrypt.email you@example.com
   sudo tljh-config add-item https.letsencrypt.domains yourinstancename.<allocation-id>.projects.jetstream-cloud.org
   sudo tljh-config show
   sudo tljh-config reload proxy
   ```
   Confirm `https.letsencrypt.domains` appears in `sudo tljh-config show` output before continuing.
2. Wait ~30–60 seconds, then reload the site using https://.

   Quick terminal checks (faster than refreshing the browser repeatedly):

   ```bash
   sudo ss -ltnp | grep -E ':80|:443'
   curl -Ik https://yourinstancename.<allocation-id>.projects.jetstream-cloud.org
   ```

   The `curl -Ik` check can return `200`, `302`, or `405`, and all of these indicate the HTTPS endpoint is reachable.

   If certificate issuance fails, check the logs:

   ```bash
   sudo journalctl -u traefik --since "15 minutes ago" | grep -iE "acme|error|443|certificate|challenge"
   ```

Tips:

- Make sure ports 80 and 443 are open in your Jetstream security group (they are open by default for new projects; adjust only if you customized network policies).
- If you later attach a custom domain, add it with another `add-item` command and reload the proxy again.
- If `https.letsencrypt.domains` is missing from `sudo tljh-config show`, run the `add-item` command again, verify it appears, then reload the proxy.

## Step 4: Log in as the administrative user and set a password

1. Now log in with the `<admin-user-name>` at `https://yourinstancename.<allocation-id>.projects.jetstream-cloud.org`. Since this is the first login, you'll be prompted to set a password. Choose a strong password and store it safely. This password is now the credential for that admin user.
2. Congratulations, you have a running JupyterHub!

## Step 5: Adding more users

```{include} add-users.md

```

Next common tasks:

- [](howto-admin-admin-users)
- [](howto-user-env-user-environment-apt)
- [](howto-admin-enable-extensions)
- [](topic-installer-upgrade-actions)

Browse the full [How-To index](/howto/index) for more.

## Ask for help

Need a hand?

- For Jetstream2 specific questions (allocations, quotas, instance lifecycle, networking, etc.), use the [Jetstream support resources](https://docs.jetstream-cloud.org/overview/support/).
- For The Littlest JupyterHub usage, configuration, or upgrade questions, search or post in the [Jupyter forum TLJH category](https://discourse.jupyter.org/c/jupyterhub/tljh).
- If you believe you have found a TLJH bug or have a clear documentation improvement, open an issue (or pull request if you have a proposed fix) in the [TLJH GitHub repository](https://github.com/jupyterhub/the-littlest-jupyterhub).

When asking for help about TLJH, it is often useful to provide:

- A short description of what you were trying to do and what happened instead
- Relevant log excerpts (see [](/troubleshooting/logs))
- Your TLJH version (`sudo tljh-config show | grep version` if present in config) and the output of `lsb_release -a` for the OS
- Any custom installer flags or `tljh-config` changes you have applied

This information helps others debug and answer more quickly.
