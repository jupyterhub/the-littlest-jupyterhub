(topic-override-lab-settings)=

# Overriding Default JupyterLab Settings

If you or other users of your hub tend to use JupyterLab as your default notebook app, 
then you may want to override some of the default settings for the users of your hub. 
You can do this by creating a file `/opt/tljh/user/share/jupyter/lab/settings/overrides.json`
with the necessary settings.

This how-to guide will go through the necessary steps to set new defaults 
for all users of your `TLJH` by example: setting the default theme to **JupyterLab Dark**.

## Step 1: Change your Personal Settings

The easiest way to set new default settings for all users starts with 
configuring your own settings preferences to what you would like everyone else to have. 

1. Make sure you are in the [JupyterLab notebook interface](#howto/user-env/notebook-interfaces), 
which will look something like `http(s)://<YOUR-HUB-IP>/user/<YOUR_USERNAME/lab`.

1. Go to **Settings** in the menu bar and select **Theme -> JupyterLab Dark**.

## Step 2: Determine your Personal Settings Configuration

To set **JupyterLab Dark** as the default theme for all users, we will need to create 
a `json` formatted file with the setting override. Now that you have changed your 
personal setting, you can use the **JSON Settings Editor** to get the relevant
setting snippet to add to the `overrides.json` file later.

1. Go to **Settings -> Advanced Settings Editor** then select **JSON Settings Editor** on the right.

1. Scroll down and select **Theme**. You should see the `json` formatted configuration:
   ```json
   {
      // Theme
      // @jupyterlab/apputils-extension:themes
      // Theme manager settings.
      // *************************************

      // Theme CSS Overrides
      // Override theme CSS variables by setting key-value pairs here
      "overrides": {
          "code-font-family": null,
          "code-font-size": null,
          "content-font-family": null,
          "content-font-size1": null,
          "ui-font-family": null,
          "ui-font-size1": null
      },

      // Selected Theme
      // Application-level visual styling theme
      "theme": "JupyterLab Dark",

      // Scrollbar Theming
      // Enable/disable styling of the application scrollbars
      "theme-scrollbars": false
   }
   ```

1. Determine the setting that you want to change. In this example it's the `theme` 
setting of `@jupyterlab/apputils-extension:theme` as can be seen above. 

1. Build your `json` snippet. In this case, our snippet should look like this:
   ```json
   {                                            
      "@jupyterlab/apputils-extension:themes": {
          "theme": "JupyterLab Dark"
      }
   }
   ```
   We only want to change the **Selected Theme**, so we don't need to include
   the other theme-related settings for CSS and the scrollbar.

  :::{note}
  To apply overrides for more than one setting, separate each setting by commas. For example,
  if you *also* wanted to change the interval at which the notebook autosaves your content, you can use
  ```json
  {                                            
      "@jupyterlab/apputils-extension:themes": {
          "theme": "JupyterLab Dark"
      },
    
      "@jupyterlab/docmanager-extension:plugin": {
          "autosaveInterval": 30
      }
  }
  ```
  :::

## Step 3: Apply the Overrides to the Hub

Once you have your setting snippet created, you can add it to the `overrides.json` file
so that it gets applied to all users.

1. First, create the settings directory if it doesn't already exist:
   ```bash
   sudo mkdir -p /opt/tljh/user/share/jupyter/lab/settings
   ```

1. Use `nano` to create and add content to the `overrides.json` file:
   ```bash
   sudo nano /opt/tljh/user/share/jupyter/lab/settings/overrides.json
   ```

1. Copy and paste your snippet into the file and save. 

1. Reload your configuration:
   ```bash
   sudo tljh-config reload
   ```

The new default settings should now be set for all users in your `TLJH` using the
JupyterLab notebook interface.