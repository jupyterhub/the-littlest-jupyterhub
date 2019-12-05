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
========================================================

By adding following script to the ec2 instance user data you should be 
able to configure the instance automatically, replace relevant config variables::

        #!/bin/bash
        ##############################################
        # Setup systemd environment variable overrides
        ##############################################
        mkdir /etc/systemd/system/jupyterhub.service.d

        echo "[Service]
        Environment=AWSCOGNITO_DOMAIN=${awscognito_domain}" >> /etc/systemd/system/jupyterhub.service.d/jupyterhub.conf
        
        ##############################################
        # Need to ensure oauthenticator is bumped to 0.10.0
        ##############################################
        curl https://raw.githubusercontent.com/jupyterhub/the-littlest-jupyterhub/master/bootstrap/bootstrap.py \
          | sudo python3 - \
            --admin insightadmin

        ##############################################
        # Setup aws Cognito Authenticator 
        ##############################################
        echo "c.AWSCognitoAuthenticator.client_id='${client_id}'
        c.AWSCognitoAuthenticator.client_secret='${client_secret}'
        c.AWSCognitoAuthenticator.oauth_callback_url='${callback_url}'
        c.AWSCognitoAuthenticator.username_key='username'
        c.AWSCognitoAuthenticator.oauth_logout_redirect_url='${logout_url}'" >> /opt/tljh/config/jupyterhub_config.d/awscognito.py


        tljh-config set auth.type oauthenticator.awscognito.AWSCognitoAuthenticator

        tljh-config reload

Manual configuration to use the AWS Cognito Oauthenticator
============================================================

Assuming tljh has already been installed, we need to make sure the oautheneticator module is at 0.10.0 and if not 
do a pip install oauthenticator>=0.10.0

Because the AWS Congito authenticator uses environment variables and the systemd script we need to pass the 
the AWS Cognito domain in via systemd we can do this by creating a systemd service overide file::

        /etc/systemd/system/jupyterhub.service.d/jupyterhub.conf

and add the following::

        [Service]
        Environment=AWSCOGNITO_DOMAIN=https://<<my_jupyter_hub>.auth.eu-west-1.amazoncognito.com

Using your prefered editor create the config file::

        /opt/tljh/config/jupyterhub_config.d/awscognito.py

subsituting the relevant variables::

        c.AWSCognitoAuthenticator.client_id='${client_id}'
        c.AWSCognitoAuthenticator.client_secret='${client_secret}'
        c.AWSCognitoAuthenticator.oauth_callback_url='${callback_url}'
        c.AWSCognitoAuthenticator.username_key='username'
        c.AWSCognitoAuthenticator.oauth_logout_redirect_url='${logout_url}'

We'll use the ``tljh-config`` tool to configure your JupyterHub's authentication.
For more information on ``tljh-config``, see :ref:`topic/tljh-config`.

#. Tell your JupyterHub to *use* the AWS Cognito OAuthenticator for authentication::

     tljh-config set auth.type oauthenticator.awscognito.AWSCognitoAuthenticator

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
