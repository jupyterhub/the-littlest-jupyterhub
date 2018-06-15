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
import json
import subprocess
import os

c.JupyterHub.spawner_class = 'systemdspawner.SystemdSpawner'
c.JupyterHub.authenticator_class = 'dummyauthenticator.DummyAuthenticator'

here = os.getcwd()

user_environment_prefix = os.path.join(here, 'user-environment')

def ensure_conda_env(prefix):
    """
    Ensure a conda environment in the prefix
    """
    abspath = os.path.abspath(prefix)
    try:
        output = json.loads(
            subprocess.check_output(['conda', 'create', '--json', '--prefix', abspath]).decode()
        )
    except subprocess.CalledProcessError as e:
        output = json.loads(e.output.decode())
        if 'error' in output and output['error'] == f'CondaValueError: prefix already exists: {abspath}':
            return
        raise
    if 'success' in output and output['success'] == True:
        return

def ensure_conda_packages(prefix, packages):
    """
    Ensure packages are installed in the conda prefix
    """
    abspath = os.path.abspath(prefix)
    raw_output = subprocess.check_output([
        'conda', 'install',
        '--json',
        '--prefix', abspath
    ] + packages).decode()
    # `conda install` outputs JSON lines for fetch updates,
    # and a undelimited output at the end. There is no reasonable way to
    # parse this outside of this kludge.
    filtered_output = '\n'.join([
        l for l in raw_output.split('\n')
        if not l.startswith('{"fetch"')
    ])
    output = json.loads(filtered_output)
    if 'success' in output and output['success'] == True:
        return

ensure_conda_env(user_environment_prefix)
ensure_conda_packages(user_environment_prefix, ['notebook', 'jupyterhub'])

c.SystemdSpawner.extra_paths = [os.path.join(user_environment_prefix, 'bin')]
c.SystemdSpawner.use_sudo = True