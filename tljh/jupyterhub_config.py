"""
JupyterHub config for the littlest jupyterhub.
"""
import copy
import os
import yaml
from glob import glob

from systemdspawner import SystemdSpawner
from tljh import user, configurer
from tljh.config import INSTALL_PREFIX, USER_ENV_PREFIX


class CustomSpawner(SystemdSpawner):
    def start(self):
        """
        Perform system user activities before starting server
        """
        # FIXME: Move this elsewhere? Into the Authenticator?
        system_username = 'jupyter-' + self.user.name
        user.ensure_user(system_username)
        user.ensure_user_group(system_username, 'jupyterhub-users')
        if self.user.admin:
            user.ensure_user_group(system_username, 'jupyterhub-admins')
        else:
            user.remove_user_group(system_username, 'jupyterhub-admins')
        return super().start()


c.JupyterHub.spawner_class = CustomSpawner

# Use a high port so users can try this on machines with a JupyterHub already present
c.JupyterHub.hub_port = 15001

c.ConfigurableHTTPProxy.should_start = False
c.ConfigurableHTTPProxy.api_url = 'http://127.0.0.1:15002'

c.SystemdSpawner.extra_paths = [os.path.join(USER_ENV_PREFIX, 'bin')]
c.SystemdSpawner.default_shell = '/bin/bash'
# Drop the '-singleuser' suffix present in the default template
c.SystemdSpawner.unit_name_template = 'jupyter-{USERNAME}'

config_overrides_path = os.path.join(INSTALL_PREFIX, 'config.yaml')
if os.path.exists(config_overrides_path):
    with open(config_overrides_path) as f:
        config_overrides = yaml.safe_load(f)
else:
    config_overrides = {}
configurer.apply_config(config_overrides, c)

# Load arbitrary .py config files if they exist.
# This is our escape hatch
extra_configs = sorted(glob(os.path.join(INSTALL_PREFIX, 'config.d', '*.py')))
for ec in extra_configs:
    load_subconfig(ec)
