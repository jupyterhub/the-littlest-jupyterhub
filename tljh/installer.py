import argparse
import os
import secrets
import subprocess
import sys
import time
import logging
from urllib.error import HTTPError
from urllib.request import urlopen, URLError

from ruamel.yaml import YAML

from tljh import conda, systemd, traefik, user, apt
from tljh.config import INSTALL_PREFIX, HUB_ENV_PREFIX, USER_ENV_PREFIX, STATE_DIR

HERE = os.path.abspath(os.path.dirname(__file__))

rt_yaml = YAML()

# Set up logging to print to a file and to stderr
logger = logging.getLogger(__name__)

os.makedirs(INSTALL_PREFIX, exist_ok=True)
file_logger = logging.FileHandler(os.path.join(INSTALL_PREFIX, 'installer.log'))
file_logger.setFormatter(logging.Formatter('%(asctime)s %(message)s'))
logger.addHandler(file_logger)

stderr_logger = logging.StreamHandler()
stderr_logger.setFormatter(logging.Formatter('%(message)s'))
logger.addHandler(stderr_logger)
logger.setLevel(logging.INFO)


def ensure_node():
    """
    Ensure nodejs from nodesource is installed
    """
    key = b"""
-----BEGIN PGP PUBLIC KEY BLOCK-----
Version: GnuPG v1
Comment: GPGTools - https://gpgtools.org

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
=CLGF
-----END PGP PUBLIC KEY BLOCK-----
    """.strip()
    apt.trust_gpg_key(key)
    apt.add_source('nodesource', f'https://deb.nodesource.com/node_10.x', 'main')
    apt.install_packages(['nodejs'])


def ensure_chp_package(prefix):
    """
    Ensure CHP is installed
    """
    if not os.path.exists(os.path.join(prefix, 'node_modules', '.bin', 'configurable-http-proxy')):
        subprocess.check_output([
            'npm', 'install', 'configurable-http-proxy@3.1.0'
        ], cwd=prefix, stderr=subprocess.STDOUT)


def ensure_jupyterhub_service(prefix):
    """
    Ensure JupyterHub Services are set up properly
    """

    os.makedirs(STATE_DIR, mode=0o700, exist_ok=True)

    with open(os.path.join(HERE, 'systemd-units', 'jupyterhub.service')) as f:
        hub_unit_template = f.read()

    with open(os.path.join(HERE, 'systemd-units', 'configurable-http-proxy.service')) as f:
        proxy_unit_template = f.read()

    with open(os.path.join(HERE, 'systemd-units', 'traefik.service')) as f:
        traefik_unit_template = f.read()

    traefik.ensure_traefik_config(STATE_DIR)

    unit_params = dict(
        python_interpreter_path=sys.executable,
        jupyterhub_config_path=os.path.join(HERE, 'jupyterhub_config.py'),
        install_prefix=INSTALL_PREFIX,
    )
    systemd.install_unit('configurable-http-proxy.service', proxy_unit_template.format(**unit_params))
    systemd.install_unit('jupyterhub.service', hub_unit_template.format(**unit_params))
    systemd.install_unit('traefik.service', traefik_unit_template.format(**unit_params))
    systemd.reload_daemon()

    # Set up proxy / hub secret oken if it is not already setup
    proxy_secret_path = os.path.join(STATE_DIR, 'configurable-http-proxy.secret')
    if not os.path.exists(proxy_secret_path):
        with open(proxy_secret_path, 'w') as f:
            f.write('CONFIGPROXY_AUTH_TOKEN=' + secrets.token_hex(32))
        # If we are changing CONFIGPROXY_AUTH_TOKEN, restart configurable-http-proxy!
        systemd.restart_service('configurable-http-proxy')

    # Start CHP if it has already not been started
    systemd.start_service('configurable-http-proxy')
    # If JupyterHub is running, we want to restart it.
    systemd.restart_service('jupyterhub')
    systemd.restart_service('traefik')

    # Mark JupyterHub & CHP to start at boot time
    systemd.enable_service('jupyterhub')
    systemd.enable_service('configurable-http-proxy')
    systemd.enable_service('traefik')


def ensure_jupyterhub_package(prefix):
    """
    Install JupyterHub into our conda environment if needed.

    We install all python packages from PyPI as much as possible in the
    hub environment. A lot of spawners & authenticators do not have conda-forge
    packages, but do have pip packages. Keeping all python packages in the
    hub environment be installed with pip prevents accidental mixing of python
    and conda packages!
    """
    conda.ensure_pip_packages(prefix, [
        'jupyterhub==0.9.1',
        'jupyterhub-dummyauthenticator==0.3.1',
        'jupyterhub-systemdspawner==0.11',
        'jupyterhub-firstuseauthenticator==0.10',
        'jupyterhub-ldapauthenticator==1.2.2',
        'oauthenticator==0.7.3',
    ])
    traefik.ensure_traefik_binary(prefix)


def ensure_usergroups():
    """
    Sets up user groups & sudo rules
    """
    user.ensure_group('jupyterhub-admins')
    user.ensure_group('jupyterhub-users')

    logger.info("Granting passwordless sudo to JupyterHub admins...")
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
    logger.info("Setting up user environment...")
    miniconda_version = '4.5.4'
    miniconda_installer_md5 = "a946ea1d0c4a642ddf0c3a26a18bb16d"

    if not conda.check_miniconda_version(USER_ENV_PREFIX, miniconda_version):
        logger.info('Downloading & setting up user environment...')
        with conda.download_miniconda_installer(miniconda_version, miniconda_installer_md5) as installer_path:
            conda.install_miniconda(installer_path, USER_ENV_PREFIX)

    conda.ensure_conda_packages(USER_ENV_PREFIX, [
        # Conda's latest version is on conda much more so than on PyPI.
        'conda==4.5.8'
    ])

    conda.ensure_pip_packages(USER_ENV_PREFIX, [
        # JupyterHub + notebook package are base requirements for user environment
        'jupyterhub==0.9.1',
        'notebook==5.6.0',
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
    logger.info("Setting up admin users")
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
            logger.info('Waiting for JupyterHub to come up ({}/{} tries)'.format(i + 1, times))
            urlopen('http://127.0.0.1')
            return
        except HTTPError as h:
            if h.code in [404, 502, 503]:
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


def ensure_symlinks(prefix):
    """
    Ensure we symlink appropriate things into /usr/local/bin

    We add the user conda environment to PATH for notebook terminals,
    but not the hub venv. This means tljh-config is not actually accessible.

    We symlink to /usr/local/bin to 'fix' this. /usr/local/bin is the appropriate
    place, and works with sudo -E
    """
    tljh_config_src = os.path.join(prefix, 'bin', 'tljh-config')
    tljh_config_dest = '/usr/local/bin/tljh-config'
    if not os.path.exists(tljh_config_dest):
        # If this exists, we leave it alone. Do *not* remove it,
        # since we are running as root and it could be anything!
        os.symlink(tljh_config_src, tljh_config_dest)


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

    logger.info("Setting up JupyterHub...")
    ensure_node()
    ensure_jupyterhub_package(HUB_ENV_PREFIX)
    ensure_chp_package(HUB_ENV_PREFIX)
    ensure_jupyterhub_service(HUB_ENV_PREFIX)
    ensure_jupyterhub_running()
    ensure_symlinks(HUB_ENV_PREFIX)

    logger.info("Done!")


if __name__ == '__main__':
    main()
