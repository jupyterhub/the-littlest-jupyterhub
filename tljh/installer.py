"""Installation logic for TLJH"""

import argparse
import dbm
import itertools
import logging
import os
import secrets
import signal
import subprocess
import sys
import time
import warnings

import bcrypt
import pluggy
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from getpass import getpass

from tljh import (
    apt,
    conda,
    hooks,
    migrator,
    systemd,
    traefik,
    user,
    utils
)
from .config import (
    CONFIG_DIR,
    CONFIG_FILE,
    HUB_ENV_PREFIX,
    INSTALL_PREFIX,
    STATE_DIR,
    USER_ENV_PREFIX,
)
from .yaml import yaml

HERE = os.path.abspath(os.path.dirname(__file__))

logger = logging.getLogger("tljh")


def remove_chp():
    """
    Ensure CHP is not running
    """
    if os.path.exists("/etc/systemd/system/configurable-http-proxy.service"):
        if systemd.check_service_active('configurable-http-proxy.service'):
            try:
                systemd.stop_service('configurable-http-proxy.service')
            except subprocess.CalledProcessError:
                logger.info("Cannot stop configurable-http-proxy...")
        if systemd.check_service_enabled('configurable-http-proxy.service'):
            try:
                systemd.disable_service('configurable-http-proxy.service')
            except subprocess.CalledProcessError:
                logger.info("Cannot disable configurable-http-proxy...")
        try:
            systemd.uninstall_unit('configurable-http-proxy.service')
        except subprocess.CalledProcessError:
            logger.info("Cannot uninstall configurable-http-proxy...")


def ensure_jupyterhub_service(prefix):
    """
    Ensure JupyterHub Services are set up properly
    """

    remove_chp()
    systemd.reload_daemon()

    with open(os.path.join(HERE, 'systemd-units', 'jupyterhub.service')) as f:
        hub_unit_template = f.read()


    with open(os.path.join(HERE, 'systemd-units', 'traefik.service')) as f:
        traefik_unit_template = f.read()

    #Set up proxy / hub secret token if it is not already setup
    proxy_secret_path = os.path.join(STATE_DIR, 'traefik-api.secret')
    if not os.path.exists(proxy_secret_path):
        with open(proxy_secret_path, 'w') as f:
            f.write(secrets.token_hex(32))

    traefik.ensure_traefik_config(STATE_DIR)

    unit_params = dict(
        python_interpreter_path=sys.executable,
        jupyterhub_config_path=os.path.join(HERE, 'jupyterhub_config.py'),
        install_prefix=INSTALL_PREFIX,
    )
    systemd.install_unit('jupyterhub.service', hub_unit_template.format(**unit_params))
    systemd.install_unit('traefik.service', traefik_unit_template.format(**unit_params))
    systemd.reload_daemon()

    # If JupyterHub is running, we want to restart it.
    systemd.restart_service('jupyterhub')
    systemd.restart_service('traefik')

    # Mark JupyterHub & traefik to start at boot time
    systemd.enable_service('jupyterhub')
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
    # Install pycurl. JupyterHub prefers pycurl over SimpleHTTPClient automatically
    # pycurl is generally more bugfree - see https://github.com/jupyterhub/the-littlest-jupyterhub/issues/289
    # build-essential is also generally useful to everyone involved, and required for pycurl
    apt.install_packages([
        'libssl-dev',
        'libcurl4-openssl-dev',
        'build-essential'
    ])
    conda.ensure_pip_packages(prefix, [
        'pycurl==7.43.*'
    ])

    conda.ensure_pip_packages(
        prefix,
        [
            "jupyterhub==1.2.2",
            "jupyterhub-dummyauthenticator==0.3.1",
            "jupyterhub-systemdspawner==0.15",
            "jupyterhub-firstuseauthenticator==0.14.1",
            "jupyterhub-nativeauthenticator==0.0.5",
            "jupyterhub-ldapauthenticator==1.3.0",
            "jupyterhub-tmpauthenticator==0.6",
            "oauthenticator==0.10.0",
            "jupyterhub-idle-culler==1.0",
            "chardet==3.0.4",
        ],
    )
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

    miniforge_version = '4.8.5-2'
    miniforge_installer_sha256 = "67e15be1628cfc191d95f84b7de4db82d11f32953245c913c7846a85fdbe68bc"


    if not conda.check_miniconda_version(USER_ENV_PREFIX, "4.8.5"):
        logger.info('Downloading & setting up user environment...')
        # Conda 4.8.5 and Python 3.8.6
        installer_url = "https://github.com/conda-forge/miniforge/releases/download/{miniforge_version}/Miniforge3-{miniforge_version}-Linux-x86_64.sh"
        with conda.download_miniconda_installer(installer_url, miniforge_installer_sha256) as installer_path:
            conda.install_miniconda(installer_path, USER_ENV_PREFIX)

    conda.ensure_conda_packages(USER_ENV_PREFIX, [
        'conda==4.8.5'
    ])

    conda.ensure_pip_requirements(
        USER_ENV_PREFIX,
        os.path.join(HERE, 'requirements-base.txt'),
    )

    if user_requirements_txt_file:
        # FIXME: This currently fails hard, should fail soft and not abort installer
        conda.ensure_pip_requirements(USER_ENV_PREFIX, user_requirements_txt_file)


def ensure_admins(admin_password_list):
    """
    Setup given list of users as admins.
    """
    os.makedirs(STATE_DIR, mode=0o700, exist_ok=True)

    if not admin_password_list:
        return
    logger.info("Setting up admin users")
    config_path = CONFIG_FILE
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            config = yaml.load(f)
    else:
        config = {}

    config['users'] = config.get('users', {})

    db_passw = os.path.join(STATE_DIR, 'passwords.dbm')

    admins = []
    for admin_password_entry in admin_password_list:
        for admin_password_pair in admin_password_entry:
            if ":" in admin_password_pair:
                admin, password = admin_password_pair.split(':')
                admins.append(admin)
                # Add admin:password to the db
                password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
                with dbm.open(db_passw, 'c', 0o600) as db:
                    db[admin] = password
            else:
                admins.append(admin_password_pair)
    config['users']['admin'] = admins

    with open(config_path, 'w+') as f:
        yaml.dump(config, f)


def ensure_jupyterhub_running(times=20):
    """
    Ensure that JupyterHub is up and running

    Loops given number of times, waiting a second each.
    """

    for i in range(times):
        try:
            logger.info(f'Waiting for JupyterHub to come up ({i + 1}/{tries} tries)')
            # Because we don't care at this level that SSL is valid, we can suppress
            # InsecureRequestWarning for this request.
            with warnings.catch_warnings():
                warnings.filterwarnings("ignore", category=InsecureRequestWarning)
                requests.get('http://127.0.0.1', verify=False)
            return
        except requests.HTTPError as h:
            if h.response.status_code in [404, 502, 503]:
                # May be transient
                time.sleep(1)
                continue
            # Everything else should immediately abort
            raise
        except requests.ConnectionError:
                # Hub isn't up yet, sleep & loop
                time.sleep(1)
                continue
        except Exception:
            # Everything else should immediately abort
            raise

    raise Exception(f"Installation failed: JupyterHub did not start in {times}s")


def ensure_symlinks(prefix):
    """
    Ensure we symlink appropriate things into /usr/bin

    We add the user conda environment to PATH for notebook terminals,
    but not the hub venv. This means tljh-config is not actually accessible.

    We symlink to /usr/bin and not /usr/local/bin, since /usr/local/bin is
    not place, and works with sudo -E in sudo's search $PATH. We can work
    around this with sudo -E and extra entries in the sudoers file, but this
    is far more secure at the cost of upsetting some FHS purists.
    """
    tljh_config_src = os.path.join(prefix, 'bin', 'tljh-config')
    tljh_config_dest = '/usr/bin/tljh-config'
    if os.path.exists(tljh_config_dest):
        if os.path.realpath(tljh_config_dest) != tljh_config_src:
            #  tljh-config exists that isn't ours. We should *not* delete this file,
            # instead we throw an error and abort. Deleting files owned by other people
            # while running as root is dangerous, especially with symlinks involved.
            raise FileExistsError(f'/usr/bin/tljh-config exists but is not a symlink to {tljh_config_src}')
        else:
            # We have a working symlink, so do nothing
            return
    os.symlink(tljh_config_src, tljh_config_dest)


def setup_plugins(plugins=None):
    """
    Install plugins & setup a pluginmanager
    """
    # Install plugins
    if plugins:
        conda.ensure_pip_packages(HUB_ENV_PREFIX, plugins)

    # Set up plugin infrastructure
    pm = pluggy.PluginManager('tljh')
    pm.add_hookspecs(hooks)
    pm.load_setuptools_entrypoints('tljh')

    return pm


def run_plugin_actions(plugin_manager):
    """
    Run installer hooks defined in plugins
    """
    hook = plugin_manager.hook
    # Install apt packages
    apt_packages = list(set(itertools.chain(*hook.tljh_extra_apt_packages())))
    if apt_packages:
        logger.info(f'Installing {len(apt_packages)} apt packages collected from plugins: {" ".join(apt_packages)}')
        apt.install_packages(apt_packages)

    # Install hub pip packages
    hub_pip_packages = list(set(itertools.chain(*hook.tljh_extra_hub_pip_packages())))
    if hub_pip_packages:
        logger.info(f'Installing {len(hub_pip_packages)} hub pip packages collected from plugins: {" ".join(hub_pip_packages)}')
        conda.ensure_pip_packages(HUB_ENV_PREFIX, hub_pip_packages)

    # Install conda packages
    conda_packages = list(set(itertools.chain(*hook.tljh_extra_user_conda_packages())))
    if conda_packages:
        logger.info(f'Installing {len(conda_packages)} user conda packages collected from plugins: {" ".join(conda_packages)}')
        conda.ensure_conda_packages(USER_ENV_PREFIX, conda_packages)

    # Install pip packages
    user_pip_packages = list(set(itertools.chain(*hook.tljh_extra_user_pip_packages())))
    if user_pip_packages:
        logger.info(f'Installing {len(user_pip_packages)} user pip packages collected from plugins: {" ".join(user_pip_packages)}')
        conda.ensure_pip_packages(USER_ENV_PREFIX, user_pip_packages)

    # Custom post install actions
    hook.tljh_post_install()


def ensure_config_yaml(plugin_manager):
    """
    Ensure we have a config.yaml present
    """
    # ensure config dir exists and is private
    for path in [CONFIG_DIR, os.path.join(CONFIG_DIR, 'jupyterhub_config.d')]:
        os.makedirs(path, mode=0o700, exist_ok=True)

    migrator.migrate_config_files()

    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            config = yaml.load(f)
    else:
        config = {}

    hook = plugin_manager.hook
    hook.tljh_config_post_install(config=config)

    with open(CONFIG_FILE, 'w+') as f:
        yaml.dump(config, f)


def main():
    from .log import init_logging
    init_logging()

    argparser = argparse.ArgumentParser()
    argparser.add_argument(
        '--admin',
        nargs='*',
        action='append',
        help='List of usernames set to be admin'
    )
    argparser.add_argument(
        '--user-requirements-txt-url',
        help='URL to a requirements.txt file that should be installed in the user environment'
    )
    argparser.add_argument(
        '--plugin',
        nargs='*',
        help='Plugin pip-specs to install'
    )
    argparser.add_argument(
        '--progress-page-server-pid',
        type=int,
        help='The pid of the progress page server'
    )

    args = argparser.parse_args()

    pm = setup_plugins(args.plugin)

    ensure_config_yaml(pm)
    ensure_admins(args.admin)
    ensure_usergroups()
    ensure_user_environment(args.user_requirements_txt_url)

    logger.info("Setting up JupyterHub...")
    ensure_jupyterhub_package(HUB_ENV_PREFIX)

    # Stop the http server with the progress page before traefik starts
    if args.progress_page_server_pid:
        try:
            os.kill(args.progress_page_server_pid, signal.SIGINT)
            # Log and print the message to make testing easier
            print("Progress page server stopped successfully.")
        except Exception as e:
            logger.error(f"Couldn't stop the progress page server. Exception was {e}.")
            pass

    ensure_jupyterhub_service(HUB_ENV_PREFIX)
    ensure_jupyterhub_running()
    ensure_symlinks(HUB_ENV_PREFIX)

    # Run installer plugins last
    run_plugin_actions(pm)

    logger.info("Done!")


if __name__ == '__main__':
    main()
