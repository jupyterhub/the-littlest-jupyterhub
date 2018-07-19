import sys
import os
import tljh.systemd as systemd
import tljh.conda as conda
from urllib.error import HTTPError
from urllib.request import urlopen, URLError
from tljh import user
import secrets
import argparse
import time
from ruamel.yaml import YAML

INSTALL_PREFIX = os.environ.get('TLJH_INSTALL_PREFIX', '/opt/tljh')
HUB_ENV_PREFIX = os.path.join(INSTALL_PREFIX, 'hub')
USER_ENV_PREFIX = os.path.join(INSTALL_PREFIX, 'user')

HERE = os.path.abspath(os.path.dirname(__file__))

rt_yaml = YAML()


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
    proxy_secret_path = os.path.join(HUB_ENV_PREFIX, 'state', 'configurable-http-proxy.secret')
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

    We install all python packages from PyPI as much as possible in the
    hub environment. A lot of spawners & authenticators do not have conda-forge
    packages, but do have pip packages. Keeping all python packages in the
    hub environment be installed with pip prevents accidental mixing of python
    and conda packages!
    """
    conda.ensure_conda_packages(prefix, ['configurable-http-proxy==3.1.0'])
    conda.ensure_pip_packages(prefix, [
        'jupyterhub==0.9.0',
        'jupyterhub-dummyauthenticator==0.3.1',
        'jupyterhub-systemdspawner==0.11',
        'jupyterhub-firstuseauthenticator==0.10',
        'jupyterhub-ldapauthenticator==1.2.2',
        'oauthenticator==0.7.3',
    ])


def ensure_usergroups():
    """
    Sets up user groups & sudo rules
    """
    user.ensure_group('jupyterhub-admins')
    user.ensure_group('jupyterhub-users')

    print("Grainting passwordless sudo to JupyterHub admins...")
    with open('/etc/sudoers.d/jupyterhub-admins', 'w') as f:
        # JupyterHub admins should have full passwordless sudo access
        f.write('%jupyterhub-admins ALL = (ALL) NOPASSWD: ALL\n')
        # `sudo -E` should preserve the $PATH we set. This allows
        # admins in jupyter terminals to do `sudo -E pip install <package>`,
        # `pip` is in the $PATH we set in jupyterhub_config.py to include the user conda env.
        f.write('Defaults exempt_group = jupyterhub-admins\n')


def ensure_user_environment(user_requirements_txt_file):
    """
    Set up user conda environment with required packages
    """
    print("Setting up user environment...")
    conda.ensure_conda_env(USER_ENV_PREFIX)
    conda.ensure_conda_packages(USER_ENV_PREFIX, [
        # Conda's latest version is on conda much more so than on PyPI.
        'conda==4.5.8'
    ])

    conda.ensure_pip_packages(USER_ENV_PREFIX, [
        # JupyterHub + notebook package are base requirements for user environment
        'jupyterhub==0.9.0',
        'notebook==5.5.0',
        # Install additional notebook frontends!
        'jupyterlab==0.32.1',
        'nteract-on-jupyter==1.8.1',
        # nbgitpuller for easily pulling in Git repositories
        'nbgitpuller==0.6.1'
    ])

    if user_requirements_txt_file:
        # FIXME: This currently fails hard, should fail soft and not abort installer
        conda.ensure_pip_requirements(USER_ENV_PREFIX, user_requirements_txt_file)


def ensure_admins(admins):
    """
    Setup given list of users as admins.
    """
    if not admins:
        return
    print("Setting up admin users")
    config_path = os.path.join(INSTALL_PREFIX, 'config.yaml')
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            config = rt_yaml.load(f)
    else:
        config = {}

    config['users'] = config.get('users', {})
    config['users']['admin'] = list(admins)

    with open(config_path, 'w+') as f:
        rt_yaml.dump(config, f)


def ensure_jupyterhub_running(times=4):
    """
    Ensure that JupyterHub is up and running

    Loops given number of times, waiting a second each.
    """

    for i in range(times):
        try:
            print('Waiting for JupyterHub to come up ({}/{} tries)'.format(i + 1, times))
            urlopen('http://127.0.0.1')
            return
        except HTTPError as h:
            if h.code in [404, 503]:
                # May be transient
                time.sleep(1)
                continue
            # Everything else should immediately abort
            raise
        except URLError as e:
            if isinstance(e.reason, ConnectionRefusedError):
                # Hub isn't up yet, sleep & loop
                time.sleep(1)
                continue
            # Everything else should immediately abort
            raise

    raise Exception("Installation failed: JupyterHub did not start in {}s".format(times))


def main():
    argparser = argparse.ArgumentParser()
    argparser.add_argument(
        '--admin',
        nargs='*',
        help='List of usernames set to be admin'
    )
    argparser.add_argument(
        '--user-requirements-txt-url',
        help='URL to a requirements.txt file that should be installed in the user enviornment'
    )

    args = argparser.parse_args()

    ensure_admins(args.admin)

    ensure_usergroups()
    ensure_user_environment(args.user_requirements_txt_url)

    print("Setting up JupyterHub...")
    ensure_jupyterhub_package(HUB_ENV_PREFIX)
    ensure_jupyterhub_service(HUB_ENV_PREFIX)
    ensure_jupyterhub_running()

    print("Done!")


if __name__ == '__main__':
    main()
