.. _howto/auth/google:

=========================
Authenticate using Google
=========================

The **Google Authenticator** lets users log into your JupyterHub using their
Google user ID / password. To do so, you'll first need to register an
application with Google, and then provide information about this
application to your ``tljh`` configuration.
See `Google's documentation <https://developers.google.com/identity/protocols/OAuth2>`_
on how to create OAUth 2.0 client credentials.


.. note::

   You'll need a Google account in order to complete these steps.

Step 1: Create a Google project
===============================

Go to `Google Developers Console <https://console.developers.google.com>`_
and create a new project:

  .. image:: ../../images/auth/google/create_new_project.png
      :alt: Create a Google project


Step 2: Set up a Google OAuth client ID and secret
==================================================

1. After creating and selecting the project:

  * Go to the credentials menu:

  .. image:: ../../images/auth/google/credentials_button.png
      :alt: Credentials menu

  * Click "Create credentials" and from the dropdown menu select **"OAuth client ID"**:

  .. image:: ../../images/auth/google/create_credentials.png
      :alt: Generate credentials

  * You will have to fill a form with:
     * **Application type**: Choose *Web application*
     * **Name**: A descriptive name for your OAuth client ID (e.g. ``tljh-client``)
     * **Authorized JavaScript origins**: Use the IP address or URL of your JupyterHub. e.g. ``http(s)://<my-tljh-url>``.
     * **Authorized redirect URIs**: Insert text with the following form::

          http(s)://<my-tljh-ip-address>/hub/oauth_callback

     * When you're done filling in the page, it should look something like this (ideally without the red warnings):

      .. image:: ../../images/auth/google/create_oauth_client_id.png
         :alt: Create a Google OAuth client ID


2. Click "Create". You'll be taken to a page with the registered application details.
3. Copy the **Client ID** and **Client Secret** from the application details
   page. You will use these later to configure your JupyterHub authenticator.

   .. image:: ../../images/auth/google/client_id_secret.png
      :alt: Your client ID and secret

.. important::

   If you are using a virtual machine from a cloud provider and
   **stop the VM**, then when you re-start the VM, the provider will likely assign a **new public
   IP address** to it. In this case, **you must update your Google application information**
   with the new IP address.

Configure your JupyterHub to use the Google Oauthenticator
==========================================================

We'll use the ``tljh-config`` tool to configure your JupyterHub's authentication.
For more information on ``tljh-config``, see :ref:`topic/tljh-config`.

#. Log in as an administrator account to your JupyterHub.
#. Open a terminal window.

   .. image:: ../../images/notebook/new-terminal-button.png
      :alt: New terminal button.

#. Configure the Google OAuthenticator to use your client ID, client secret and callback URL with the following commands::

     sudo tljh-config set auth.GoogleOAuthenticator.client_id '<my-tljh-client-id>'

   ::

     sudo tljh-config set auth.GoogleOAuthenticator.client_secret '<my-tljh-client-secret>'
   
   ::

     sudo tljh-config set auth.GoogleOAuthenticator.oauth_callback_url 'http(s)://<my-tljh-ip-address>/hub/oauth_callback'

#. Tell your JupyterHub to *use* the Google OAuthenticator for authentication::

     sudo tljh-config set auth.type oauthenticator.google.GoogleOAuthenticator

#. Restart your JupyterHub so that new users see these changes::

     sudo tljh-config reload

Confirm that the new authenticator works
========================================

#. **Open an incognito window** in your browser (do not log out until you confirm
   that the new authentication method works!)
#. Go to your JupyterHub URL.
#. You should see a Google login button like below:

   .. image:: ../../images/auth/google/login_button.png
      :alt: The Google authenticator login button.

#. After you log in with your Google credentials, you should be directed to the
   Jupyter interface used in this JupyterHub.

#. **If this does not work** you can revert back to the default
   JupyterHub authenticator by following the steps in :ref:`howto/auth/firstuse`.
