(howto-auth-awscognito)=

# Authenticate using AWS Cognito

```{warning}
This documentation has not been updated recently, and a major version of
OAuthenticator has been released since it was. Due to that, please only use this
_as a complement_ to the official [OAuthenticator documentation].

[OAuthenticator documentation]: https://oauthenticator.readthedocs.io/en/latest/tutorials/provider-specific-setup/providers/generic.html#setup-for-aws-cognito

Going onwards, the goal is to ensure we have good documentation in the
OAuthenticator project and reference that instead of maintaining similar
documentation in this project also.
```

The **AWS Cognito Authenticator** lets users log into your JupyterHub using
cognito user pools. To do so, you'll first need to register and configure a
cognito user pool and app, and then provide information about this
application to your `tljh` configuration.

## Create an AWS Cognito application

1. Create a user pool [Getting Started with User Pool](https://docs.aws.amazon.com/cognito/latest/developerguide/getting-started-with-cognito-user-pools.html).

   When you have completed creating a user pool, app, and domain you should have the following settings available to you:
   - **App client id**: From the App client page

   - **App client secret** From the App client page

   - **Callback URL** This should be the domain you are hosting you server on:

     ```
     http(s)://<my-tljh-ip-address>/hub/oauth_callback
     ```

   - **Signout URL**: This is the landing page for a user when they are not logged on:

     ```
     http(s)://<my-tljh-ip-address>
     ```

   - **Auth Domain** Create an auth domain e.g. \<my_jupyter_hub>:

     ```
     https://<<my_jupyter_hub>.auth.eu-west-1.amazoncognito.com
     ```

## Install and configure an AWS EC2 Instance with userdata

By adding following script to the ec2 instance user data you should be
able to configure the instance automatically, replace relevant placeholders:

```bash
#!/bin/bash
##############################################
# Ensure tljh is up to date
##############################################
curl -L https://tljh.jupyter.org/bootstrap.py \
  | sudo python3 - \
    --admin insightadmin

##############################################
# Setup AWS Cognito OAuthenticator
##############################################
echo > /opt/tljh/config/jupyterhub_config.d/awscognito.py <<EOF
c.GenericOAuthenticator.client_id = "[your app client ID]"
c.GenericOAuthenticator.client_secret = "[your app client secret]"
c.GenericOAuthenticator.oauth_callback_url = "https://[your-jupyterhub-host]/hub/oauth_callback"

c.GenericOAuthenticator.authorize_url = "https://your-AWSCognito-domain/oauth2/authorize"
c.GenericOAuthenticator.token_url = "https://your-AWSCognito-domain/oauth2/token"
c.GenericOAuthenticator.userdata_url = "https://your-AWSCognito-domain/oauth2/userInfo"
c.GenericOAuthenticator.logout_redirect_url = "https://your-AWSCognito-domain/oauth2/logout"

# these are always the same
c.GenericOAuthenticator.login_service = "AWS Cognito"
c.GenericOAuthenticator.username_key = "username"
c.GenericOAuthenticator.userdata_method = "POST"
EOF

tljh-config set auth.type oauthenticator.generic.GenericOAuthenticator

tljh-config reload
```

## Manual configuration to use the AWS Cognito OAuthenticator

AWS Cognito is configured as a generic OAuth provider.

Using your preferred editor create the config file:

```
/opt/tljh/config/jupyterhub_config.d/awscognito.py
```

substituting the relevant variables:

```python
c.GenericOAuthenticator.client_id = "[your app ID]"
c.GenericOAuthenticator.client_secret = "[your app Password]"
c.GenericOAuthenticator.oauth_callback_url = "https://[your-jupyterhub-host]/hub/oauth_callback"

c.GenericOAuthenticator.authorize_url = "https://your-AWSCognito-domain/oauth2/authorize"
c.GenericOAuthenticator.token_url = "https://your-AWSCognito-domain/oauth2/token"
c.GenericOAuthenticator.userdata_url = "https://your-AWSCognito-domain/oauth2/userInfo"
c.GenericOAuthenticator.logout_redirect_url = "https://your-AWSCognito-domain/oauth2/logout"

# these are always the same
c.GenericOAuthenticator.login_service = "AWS Cognito"
c.GenericOAuthenticator.username_key = "username"
c.GenericOAuthenticator.userdata_method = "POST"
```

We'll use the `tljh-config` tool to configure your JupyterHub's authentication.
For more information on `tljh-config`, see [](/topic/tljh-config).

1. Tell your JupyterHub to use the GenericOAuthenticator for authentication:

   ```
   tljh-config set auth.type oauthenticator.generic.GenericOAuthenticator
   ```

2. Restart your JupyterHub so that new users see these changes:

   ```
   sudo tljh-config reload
   ```

## Confirm that the new authenticator works

1. **Open an incognito window** in your browser (do not log out until you confirm
   that the new authentication method works!)
2. Go to your JupyterHub URL.
3. You should see an AWS Cognito login button:
4. You will likely have to create a new user (sign up) and then you should be directed to the
   Jupyter interface used in this JupyterHub.
5. **If this does not work** you can revert back to the default
   JupyterHub authenticator by following the steps in [](/howto/auth/firstuse).

## Optionally using custom claims for group mapping

If you use AWS Cognito to federate with an OIDC provider and you want to
authorize your users based on e.g. their department claim, you have to make sure
that the custom claim is provided as array.

If it is not provided as array, there is an easy fix. Just add these lines to
your `awscognito.py`:

```python
def groups_key_func(auth_state):
    return [auth_state['oauth_user']['custom:department']]

c.GenericOAuthenticator.manage_groups = True
c.GenericOAuthenticator.auth_state_groups_key = groups_key_func
c.GenericOAuthenticator.allowed_groups = ["AA BB CC", "AA BB DD"]
```
