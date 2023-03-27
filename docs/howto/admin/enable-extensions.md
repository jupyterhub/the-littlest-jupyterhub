(howto-admin-extensions)=

# Enabling Jupyter Notebook extensions

Jupyter contributed notebook
[extensions](https://jupyter-contrib-nbextensions.readthedocs.io/en/latest/index.html) are
community-contributed and maintained plug-ins to the Jupyter notebook. These extensions
serve many purposes, from [pedagogical tools](https://jupyter-contrib-nbextensions.readthedocs.io/en/latest/nbextensions/codefolding/readme.html)
to tools for [converting](https://jupyter-contrib-nbextensions.readthedocs.io/en/latest/nbextensions/latex_envs/README.html)
and [editing](https://jupyter-contrib-nbextensions.readthedocs.io/en/latest/nbextensions/spellchecker/README.html)
notebooks.

Extensions are often added and enabled through the graphical user interface of the notebook.
However, this interface only makes the extension available to the user, not all users on a
hub. Instead, to make contributed extensions available to your users, you will use the command
line. This can be completed using the terminal in the JupyterHub (or via SSH-ing into your
VM and using this terminal).

(tljh-extension-cli)=

## Enabling extensions via the command line

1. There are [multiple ways](https://jupyter-contrib-nbextensions.readthedocs.io/en/latest/install.html)
   to install contributed extensions. For this example, we will use `pip`.

   ```bash
   sudo -E pip install jupyter_contrib_nbextensions
   ```

2. Next, add the notebook extension style files to the Jupyter configuration files.

   ```bash
   sudo -E jupyter contrib nbextension install --sys-prefix
   ```

3. Then, you will enable the extensions you would like to use. The syntax for this is
   `jupyter nbextension enable` followed by the path to the desired extension's main file.
   For example, to enable [scratchpad](https://jupyter-contrib-nbextensions.readthedocs.io/en/latest/nbextensions/scratchpad/README.html),
   you would type the following:

   ```bash
   sudo -E jupyter nbextension enable scratchpad/main --sys-prefix
   ```

4. When this is completed, the enabled extension should be visible in the extension list:

   ```bash
   jupyter nbextension list
   ```

5. You can also verify the availability of the extension via its user interface in the notebook.
   For example, spellchecker adds an ABC checkmark icon to the interface.

   ```{image} ../../images/admin/enable-spellcheck.png
   :alt: spellcheck-interface-changes
   ```
