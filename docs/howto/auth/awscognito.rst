.. _howto/auth/awscognito:

==============================
Authenticate using AWS Cognito
==============================

The **AWS Cognito Authenticator** lets users log into your JupyterHub using
cognito user pools. To do so, you'll first need to register and configure a
cognito user pool and app, and then provide information about this
application to your ``tljh`` configuration.


Create an AWS Cognito application
=========================================

#. Create a user pool `Getting Started with User Pool <https://docs.aws.amazon.com/cognito/latest/developerguide/getting-started-with-cognito-user-pools.html>`_.

   When you have completed creating a user pool, app, and domain you should have the following settings available to you:

   * **App client id**: From the App client page
   * **App client secret** From the App client page
   * **Callback URL** This should be the domain you are hosting you server on::

         http(s)://<my-tljh-ip-address>/hub/oauth_callback

   * **Signout URL**: This is the landing page for a user when they are not logged on::

        http(s)://<my-tljh-ip-address>

    * **Auth Domain** Create an auth domain e.g. <my_jupyter_hub>::

        https://<<my_jupyter_hub>.auth.eu-west-1.amazoncognito.com


Install and configure an AWS EC2 Instance with userdata
=======================================================

By adding following script to the ec2 instance user data you should be
able to configure the instance automatically, replace relevant placeholders::

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

        # you may rename the login button here
        c.GenericOAuthenticator.login_service = "AWS Cognito"
        
        # if you use an AWS Cognito user pool, this is the username key
        c.GenericOAuthenticator.username_key = "username"

        EOF

        tljh-config set auth.type oauthenticator.generic.GenericOAuthenticator

        tljh-config reload

Manual configuration to use the AWS Cognito OAuthenticator
==========================================================

AWS Cognito is configured as a generic OAuth provider.

Using your preferred editor create the config file::

    /opt/tljh/config/jupyterhub_config.d/awscognito.py

substituting the relevant variables::

    c.GenericOAuthenticator.client_id = "[your app ID]"
    c.GenericOAuthenticator.client_secret = "[your app Password]"
    c.GenericOAuthenticator.oauth_callback_url = "https://[your-jupyterhub-host]/hub/oauth_callback"

    c.GenericOAuthenticator.authorize_url = "https://your-AWSCognito-domain/oauth2/authorize"
    c.GenericOAuthenticator.token_url = "https://your-AWSCognito-domain/oauth2/token"
    c.GenericOAuthenticator.userdata_url = "https://your-AWSCognito-domain/oauth2/userInfo"
    c.GenericOAuthenticator.logout_redirect_url = "https://your-AWSCognito-domain/oauth2/logout"

    # you may rename the login button here
    c.GenericOAuthenticator.login_service = "AWS Cognito"
        
    # if you use an AWS Cognito user pool, this is the username key
    c.GenericOAuthenticator.username_key = "username"

We'll use the ``tljh-config`` tool to configure your JupyterHub's authentication.
For more information on ``tljh-config``, see :ref:`topic/tljh-config`.

#. Tell your JupyterHub to use the GenericOAuthenticator for authentication::

     tljh-config set auth.type oauthenticator.generic.GenericOAuthenticator

#. Restart your JupyterHub so that new users see these changes::

     sudo tljh-config reload

Confirm that the new authenticator works
========================================

#. **Open an incognito window** in your browser (do not log out until you confirm
   that the new authentication method works!)

#. Go to your JupyterHub URL.

#. You should see an AWS Cognito login button:

#. You will likely have to create a new user (sign up) and then you should be directed to the
   Jupyter interface used in this JupyterHub.

#. **If this does not work** you can revert back to the default
   JupyterHub authenticator by following the steps in :ref:`howto/auth/firstuse`.
   
Using custom claims for group mapping
=====================================

If you use AWS Cognito to federate with an OIDC provider and you want to authorize
your users based on e.g. their department claim, you have to make sure that the custom
claim is provided as array.

If it is not provided as array, there is an easy fix. Just add these lines to your ``awscognito.py``::

    def claim_groups_key_func(user_data_resp_json):
        return [user_data_resp_json['custom:department']]
    
    c.GenericOAuthenticator.claim_groups_key = claim_groups_key_func
    c.GenericOAuthenticator.allowed_groups = ["AA BB CC", "AA BB DD"]
