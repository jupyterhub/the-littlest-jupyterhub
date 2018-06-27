"""
JupyterHub config for the littlest jupyterhub.

This is run on startup & restarts. This file has the following
responsibilities:

1. Set up & maintain user conda environment
2. Configure JupyterHub from YAML file

This code will run as an unprivileged user, but with unlimited
sudo access. Code here can block, since it all runs before JupyterHub
starts.
"""
from tljh import conda
import os

INSTALL_PREFIX = os.environ.get('TLJH_INSTALL_PREFIX', '/opt/tljh')
USER_ENV_PREFIX = os.path.join(INSTALL_PREFIX, 'user')

c.JupyterHub.spawner_class = 'systemdspawner.SystemdSpawner'
c.JupyterHub.authenticator_class = 'dummyauthenticator.DummyAuthenticator'

c.SystemdSpawner.extra_paths = [os.path.join(USER_ENV_PREFIX, 'bin')]
c.SystemdSpawner.use_sudo = True

c.SystemdSpawner.dynamic_users = True
