import sys
import os
import tljh.systemd as systemd
import tljh.conda as conda
from tljh import user
import secrets

INSTALL_PREFIX = os.environ.get('TLJH_INSTALL_PREFIX', '/opt/tljh')
HUB_ENV_PREFIX = os.path.join(INSTALL_PREFIX, 'hub')
USER_ENV_PREFIX = os.path.join(INSTALL_PREFIX, 'user')

HERE = os.path.abspath(os.path.dirname(__file__))


def ensure_jupyterhub_service(prefix):
    """
    Ensure JupyterHub & CHP Services are set up properly
    """
    with open(os.path.join(HERE, 'systemd-units', 'jupyterhub.service')) as f:
        hub_unit_template = f.read()

    with open(os.path.join(HERE, 'systemd-units', 'configurable-http-proxy.service')) as f:
        proxy_unit_template = f.read()

    unit_params = dict(
        python_interpreter_path=sys.executable,
        jupyterhub_config_path=os.path.join(HERE, 'jupyterhub_config.py'),
        install_prefix=INSTALL_PREFIX
    )
    systemd.install_unit('configurable-http-proxy.service', proxy_unit_template.format(**unit_params))
    systemd.install_unit('jupyterhub.service', hub_unit_template.format(**unit_params))
    systemd.reload_daemon()

    # Set up proxy / hub secret oken if it is not already setup
    # FIXME: Check umask here properly
    proxy_secret_path = os.path.join(INSTALL_PREFIX, 'configurable-http-proxy.secret')
    if not os.path.exists(proxy_secret_path):
        with open(proxy_secret_path, 'w') as f:
            f.write('CONFIGPROXY_AUTH_TOKEN=' + secrets.token_hex(32))
        # If we are changing CONFIGPROXY_AUTH_TOKEN, restart configurable-http-proxy!
        systemd.restart_service('configurable-http-proxy')

    os.makedirs(os.path.join(INSTALL_PREFIX, 'hub', 'state'), mode=0o700, exist_ok=True)
    # Start CHP if it has already not been started
    systemd.start_service('configurable-http-proxy')
    # If JupyterHub is running, we want to restart it.
    systemd.restart_service('jupyterhub')

    # Mark JupyterHub & CHP to start at boot ime
    systemd.enable_service('jupyterhub')
    systemd.enable_service('configurable-http-proxy')


def ensure_jupyterhub_package(prefix):
    """
    Install JupyterHub into our conda environment if needed.

    Conda constructor does not play well with conda-forge, so we can ship this
    with constructor
    """
    # FIXME: Use fully deterministic package lists here
    conda.ensure_conda_packages(prefix, ['jupyterhub==0.9.0'])
    conda.ensure_pip_packages(prefix, [
        'jupyterhub-dummyauthenticator==0.3.1',
        'jupyterhub-systemdspawner==0.9.12',
    ])


ensure_jupyterhub_package(HUB_ENV_PREFIX)
ensure_jupyterhub_service(HUB_ENV_PREFIX)

user.ensure_group('jupyterhub-admins')
user.ensure_group('jupyterhub-users')

with open('/etc/sudoers.d/jupyterhub-admins', 'w') as f:
    f.write('%jupyterhub-admins ALL = (ALL) NOPASSWD: ALL')

conda.ensure_conda_env(USER_ENV_PREFIX)
conda.ensure_conda_packages(USER_ENV_PREFIX, [
    'jupyterhub==0.9.0',
    'notebook==5.5.0',
    'jupyterlab==0.32.1',
    'conda==4.5.4'
])
