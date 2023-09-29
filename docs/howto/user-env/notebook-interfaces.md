(howto/user-env/notebook-interfaces)=

# Change default user interface

By default a user starting a server will see the JupyterLab interface. This can
be changed with TLJH config `user_environment.default_app` or with the
JupyterHub config
{external:py:attr}`jupyterhub.spawner.Spawner.default_url` directly.

The TLJH config supports the options `jupyterlab` and `classic`, which
translates to a `Spawner.default_url` config of `/lab` and `/tree`.

Both these interfaces are also shipped with TLJH by default. You can try them
temporarily, or set them to be the default interface whenever you login.

## Trying an alternate interface temporarily

When you log in and start your server, by default the URL in your browser will
be something like `/user/<username>/lab`. The `/lab` is what tells the jupyter
server to give you the JupyterLab user interface.

As an example, you can update the URL to not end with `/lab`, but instead end
with `/tree` to temporarily switch to the classic interface.

## Changing the default user interface using TLJH config

You can change the default url, and therefore the interface users get when they
log in by modifying TLJH config as an admin user.

1.  To launch the classic notebook interface when users log in, run the
    following in the admin console:

    ```bash
    sudo tljh-config set user_environment.default_app classic
    ```

1.  To launch JupyterLab when users log in, run the following in an admin
    console:

    ```bash
    sudo tljh-config set user_environment.default_app jupyterlab
    ```

1.  Apply the changes by restarting JupyterHub. This should not disrupt
    current users.

    ```bash
    sudo tljh-config reload hub
    ```

    If this causes problems, check the [logs](#troubleshoot-logs-jupyterhub) for
    clues on what went wrong.

Users might have to restart their servers from control panel to get the
new interface.
