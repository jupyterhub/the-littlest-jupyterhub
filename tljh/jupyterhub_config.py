"""
JupyterHub config for the littlest jupyterhub.
"""

from glob import glob
import os

from tljh import configurer
from tljh.config import INSTALL_PREFIX, USER_ENV_PREFIX, CONFIG_DIR
from tljh.utils import get_plugin_manager
from tljh.user_creating_spawner import UserCreatingSpawner
from jupyterhub_traefik_proxy import TraefikTomlProxy

c.JupyterHub.spawner_class = UserCreatingSpawner

# leave users running when the Hub restarts
c.JupyterHub.cleanup_servers = False

# Use a high port so users can try this on machines with a JupyterHub already present
c.JupyterHub.hub_port = 15001

c.TraefikTomlProxy.should_start = False

dynamic_conf_file_path = os.path.join(INSTALL_PREFIX, "state", "rules", "rules.toml")
c.TraefikTomlProxy.toml_dynamic_config_file = dynamic_conf_file_path
c.JupyterHub.proxy_class = TraefikTomlProxy

c.SystemdSpawner.extra_paths = [os.path.join(USER_ENV_PREFIX, "bin")]
c.SystemdSpawner.default_shell = "/bin/bash"
# Drop the '-singleuser' suffix present in the default template
c.SystemdSpawner.unit_name_template = "jupyter-{USERNAME}"

tljh_config = configurer.load_config()
configurer.apply_config(tljh_config, c)

# Let TLJH hooks modify `c` if they want

# Call our custom configuration plugin
pm = get_plugin_manager()
pm.hook.tljh_custom_jupyterhub_config(c=c)

# Load arbitrary .py config files if they exist.
# This is our escape hatch
extra_configs = sorted(glob(os.path.join(CONFIG_DIR, "jupyterhub_config.d", "*.py")))
for ec in extra_configs:
    load_subconfig(ec)
