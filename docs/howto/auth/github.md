(howto-auth-github)=

# Authenticate using GitHub Usernames

```{warning}
This documentation has not been updated recently, and a major version of
OAuthenticator has been released since it was. Due to that, please only use this
_as a complement_ to the official [OAuthenticator documentation].

[OAuthenticator documentation]: https://oauthenticator.readthedocs.io/en/latest/tutorials/provider-specific-setup/providers/github.html

Going onwards, the goal is to ensure we have good documentation in the
OAuthenticator project and reference that instead of maintaining similar
documentation in this project also.
```

The **GitHub Authenticator** lets users log into your JupyterHub using their
GitHub user ID / password. To do so, you'll first need to register an
application with GitHub, and then provide information about this
application to your `tljh` configuration.

:::{note}
You'll need a GitHub account in order to complete these steps.
:::

## Step 1: Create a GitHub application

1. Go to the [GitHub OAuth app creation page](https://github.com/settings/applications/new).
   - **Application name**: Choose a descriptive application name (e.g. `tljh`)

   - **Homepage URL**: Use the IP address or URL of your JupyterHub. e.g. `` http(s)://<my-tljh-url>` ``.

   - **Application description**: Use any description that you like.

   - **Authorization callback URL**: Insert text with the following form:

     ```
     http(s)://<my-tljh-ip-address>/hub/oauth_callback
     ```

   - When you're done filling in the page, it should look something like this:

     ```{image} ../../images/auth/github/create_application.png
     :alt: Create a GitHub OAuth application
     ```

2. Click "Register application". You'll be taken to a page with the registered application details.

3. Copy the **Client ID** and **Client Secret** from the application details
   page. You will use these later to configure your JupyterHub authenticator.

   ```{image} ../../images/auth/github/client_id_secret.png
   :alt: Your client ID and secret
   ```

:::{important}
If you are using a virtual machine from a cloud provider and
**stop the VM**, then when you re-start the VM, the provider will likely assign a **new public
IP address** to it. In this case, **you must update your GitHub application information**
with the new IP address.
:::

## Configure your JupyterHub to use the GitHub Oauthenticator

We'll use the `tljh-config` tool to configure your JupyterHub's authentication.
For more information on `tljh-config`, see [](/topic/tljh-config).

1. Log in as an administrator account to your JupyterHub.

2. Open a terminal window.

   ```{image} ../../images/notebook/new-terminal-button.png
   :alt: New terminal button.
   ```

3. Configure the GitHub OAuthenticator to use your client ID, client secret and callback URL with the following commands:

   ```
   sudo tljh-config set auth.GitHubOAuthenticator.client_id '<my-tljh-client-id>'
   ```

   ```
   sudo tljh-config set auth.GitHubOAuthenticator.client_secret '<my-tljh-client-secret>'
   ```

   ```
   sudo tljh-config set auth.GitHubOAuthenticator.oauth_callback_url 'http(s)://<my-tljh-ip-address>/hub/oauth_callback'
   ```

4. Tell your JupyterHub to _use_ the GitHub OAuthenticator for authentication:

   ```
   sudo tljh-config set auth.type github
   ```

5. Tell JupyterHub which users to allow, if you haven't already:

   ```
   sudo tljh-config add-item users.allowed good-user_1
   ```

6. Restart your JupyterHub so that new users see these changes:

   ```
   sudo tljh-config reload
   ```

## Confirm that the new authenticator works

1. **Open an incognito window** in your browser (do not log out until you confirm
   that the new authentication method works!)

2. Go to your JupyterHub URL.

3. You should see a GitHub login button like below:

   ```{image} ../../images/auth/github/login_button.png
   :alt: The GitHub authenticator login button.
   ```

4. After you log in with your GitHub credentials, you should be directed to the
   Jupyter interface used in this JupyterHub.

5. **If this does not work** you can revert back to the default
   JupyterHub authenticator by following the steps in [](/howto/auth/firstuse).
