(howto-auth-dummy)=

# Authenticate users with temporary accounts automatically

```{warning}
The **Temporary Authenticator** lets _any_ user access JupyterHub without logging in.
This authenticator is designed for open deployments and should be used with caution
in environments where access control is important.
```

## Enabling the authenticator

1. Install the TmpAuthenticator package:

   ```bash
   sudo pip3 install jupyterhub-tmpauthenticator
   ```

2. Enable the authenticator and configure it to allow all users:

   ```bash
   sudo tljh-config set auth.type tmpauthenticator.TmpAuthenticator
   sudo tljh-config set auth.TmpAuthenticator.allow_all 'True'
   ```

3. Reload the configuration to apply changes:

   ```bash
   sudo tljh-config reload
   ```

## How it works

The Temporary Authenticator:
- Gives anyone who visits the JupyterHub landing page a user account without requiring login
- Automatically spawns a single-user server for each visitor
- Redirects users directly to their server without requiring them to click additional buttons

This is particularly useful for temporary deployments, workshops, or demonstration environments where ease of access is more important than user authentication.

## Configuration options

While the default configuration works for most temporary deployments, you can customize the behavior:

### Disabling automatic login

By default, TmpAuthenticator automatically logs users in. You can change this behavior:

```bash
sudo tljh-config set auth.TmpAuthenticator.auto_login 'False'
sudo tljh-config reload
```

With `auto_login` set to `False`, users will see a home page with a "Sign in" button.

### Customizing the login button text

If you've disabled automatic login, you can customize the text shown on the login button:

```bash
sudo tljh-config set auth.TmpAuthenticator.login_service 'Temporary Access'
sudo tljh-config reload
```
