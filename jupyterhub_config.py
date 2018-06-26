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

c.JupyterHub.spawner_class = 'systemdspawner.SystemdSpawner'
c.JupyterHub.authenticator_class = 'dummyauthenticator.DummyAuthenticator'

here = os.getcwd()

user_environment_prefix = os.path.join(here, 'user-environment')

conda.ensure_conda_env(user_environment_prefix)
conda.ensure_conda_packages(user_environment_prefix, ['notebook', 'jupyterhub'])

c.SystemdSpawner.extra_paths = [os.path.join(user_environment_prefix, 'bin')]
c.SystemdSpawner.use_sudo = True
