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

from tljh import (
    apt,
    conda,
    hooks,
    migrator,
    systemd,
    traefik,
    user,
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
        if systemd.check_service_active("configurable-http-proxy.service"):
            try:
                systemd.stop_service("configurable-http-proxy.service")
            except subprocess.CalledProcessError:
                logger.info("Cannot stop configurable-http-proxy...")
        if systemd.check_service_enabled("configurable-http-proxy.service"):
            try:
                systemd.disable_service("configurable-http-proxy.service")
            except subprocess.CalledProcessError:
                logger.info("Cannot disable configurable-http-proxy...")
        try:
            systemd.uninstall_unit("configurable-http-proxy.service")
        except subprocess.CalledProcessError:
            logger.info("Cannot uninstall configurable-http-proxy...")


def ensure_jupyterhub_service(prefix):
    """
    Ensure JupyterHub Services are set up properly
    """

    remove_chp()
    systemd.reload_daemon()

    with open(os.path.join(HERE, "systemd-units", "jupyterhub.service")) as f:
        hub_unit_template = f.read()

    with open(os.path.join(HERE, "systemd-units", "traefik.service")) as f:
        traefik_unit_template = f.read()

    # Set up proxy / hub secret token if it is not already setup
    proxy_secret_path = os.path.join(STATE_DIR, "traefik-api.secret")
    if not os.path.exists(proxy_secret_path):
        with open(proxy_secret_path, "w") as f:
            f.write(secrets.token_hex(32))

    traefik.ensure_traefik_config(STATE_DIR)

    unit_params = dict(
        python_interpreter_path=sys.executable,
        jupyterhub_config_path=os.path.join(HERE, "jupyterhub_config.py"),
        install_prefix=INSTALL_PREFIX,
    )
    systemd.install_unit("jupyterhub.service", hub_unit_template.format(**unit_params))
    systemd.install_unit("traefik.service", traefik_unit_template.format(**unit_params))
    systemd.reload_daemon()

    # If JupyterHub is running, we want to restart it.
    systemd.restart_service("jupyterhub")
    systemd.restart_service("traefik")

    # Mark JupyterHub & traefik to start at boot time
    systemd.enable_service("jupyterhub")
    systemd.enable_service("traefik")


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
    apt.install_packages(["libssl-dev", "libcurl4-openssl-dev", "build-essential"])
    conda.ensure_pip_packages(prefix, ["pycurl==7.*"], upgrade=True)

    conda.ensure_pip_packages(
        prefix,
        [
            "jupyterhub==1.*",
            "jupyterhub-systemdspawner==0.15.*",
            "jupyterhub-firstuseauthenticator==1.*",
            "jupyterhub-nativeauthenticator==1.*",
            "jupyterhub-ldapauthenticator==1.*",
            "jupyterhub-tmpauthenticator==0.6.*",
            "oauthenticator==14.*",
            "jupyterhub-idle-culler==1.*",
            "git+https://github.com/yuvipanda/jupyterhub-configurator@317759e17c8e48de1b1352b836dac2a230536dba",
        ],
        upgrade=True,
    )
    traefik.ensure_traefik_binary(prefix)


def ensure_usergroups():
    """
    Sets up user groups & sudo rules
    """
    user.ensure_group("jupyterhub-admins")
    user.ensure_group("jupyterhub-users")

    logger.info("Granting passwordless sudo to JupyterHub admins...")
    with open("/etc/sudoers.d/jupyterhub-admins", "w") as f:
        # JupyterHub admins should have full passwordless sudo access
        f.write("%jupyterhub-admins ALL = (ALL) NOPASSWD: ALL\n")
        # `sudo -E` should preserve the $PATH we set. This allows
        # admins in jupyter terminals to do `sudo -E pip install <package>`,
        # `pip` is in the $PATH we set in jupyterhub_config.py to include the user conda env.
        f.write("Defaults exempt_group = jupyterhub-admins\n")


def ensure_user_environment(user_requirements_txt_file):
    """
    Set up user conda environment with required packages
    """
    logger.info("Setting up user environment...")

    miniconda_old_version = "4.5.4"
    miniconda_new_version = "4.7.10"
    # Install mambaforge using an installer from
    # https://github.com/conda-forge/miniforge/releases
    mambaforge_new_version = "4.10.3-7"
    # Check system architecture, set appropriate installer checksum
    if os.uname().machine == "aarch64":
        installer_sha256 = (
            "ac95f137b287b3408e4f67f07a284357b1119ee157373b788b34e770ef2392b2"
        )
    elif os.uname().machine == "x86_64":
        installer_sha256 = (
            "fc872522ec427fcab10167a93e802efaf251024b58cc27b084b915a9a73c4474"
        )
    # Check OS, set appropriate string for conda installer path
    if os.uname().sysname != "Linux":
        raise OSError("TLJH is only supported on Linux platforms.")
    # Then run `mamba --version` to get the conda and mamba versions
    # Keep these in sync with tests/test_conda.py::prefix
    mambaforge_conda_new_version = "4.10.3"
    mambaforge_mamba_version = "0.16.0"

    if conda.check_miniconda_version(USER_ENV_PREFIX, mambaforge_conda_new_version):
        conda_version = "4.10.3"
    elif conda.check_miniconda_version(USER_ENV_PREFIX, miniconda_new_version):
        conda_version = "4.8.1"
    elif conda.check_miniconda_version(USER_ENV_PREFIX, miniconda_old_version):
        conda_version = "4.5.8"
    # If no prior miniconda installation is found, we can install a newer version
    else:
        logger.info("Downloading & setting up user environment...")
        installer_url = "https://github.com/conda-forge/miniforge/releases/download/{v}/Mambaforge-{v}-Linux-{arch}.sh".format(
            v=mambaforge_new_version, arch=os.uname().machine
        )
        with conda.download_miniconda_installer(
            installer_url, installer_sha256
        ) as installer_path:
            conda.install_miniconda(installer_path, USER_ENV_PREFIX)
        conda_version = "4.10.3"

    conda.ensure_conda_packages(
        USER_ENV_PREFIX,
        [
            # Conda's latest version is on conda much more so than on PyPI.
            "conda==" + conda_version,
            "mamba==" + mambaforge_mamba_version,
        ],
    )

    conda.ensure_pip_requirements(
        USER_ENV_PREFIX,
        os.path.join(HERE, "requirements-base.txt"),
        upgrade=True,
    )

    if user_requirements_txt_file:
        # FIXME: This currently fails hard, should fail soft and not abort installer
        conda.ensure_pip_requirements(
            USER_ENV_PREFIX,
            user_requirements_txt_file,
            upgrade=True,
        )


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
        with open(config_path) as f:
            config = yaml.load(f)
    else:
        config = {}

    config["users"] = config.get("users", {})

    db_passw = os.path.join(STATE_DIR, "passwords.dbm")

    admins = []
    for admin_password_entry in admin_password_list:
        for admin_password_pair in admin_password_entry:
            if ":" in admin_password_pair:
                admin, password = admin_password_pair.split(":")
                admins.append(admin)
                # Add admin:password to the db
                password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
                with dbm.open(db_passw, "c", 0o600) as db:
                    db[admin] = password
            else:
                admins.append(admin_password_pair)
    config["users"]["admin"] = admins

    with open(config_path, "w+") as f:
        yaml.dump(config, f)


def ensure_jupyterhub_running(times=20):
    """
    Ensure that JupyterHub is up and running

    Loops given number of times, waiting a second each.
    """

    for i in range(times):
        try:
            logger.info(f"Waiting for JupyterHub to come up ({i + 1}/{times} tries)")
            # Because we don't care at this level that SSL is valid, we can suppress
            # InsecureRequestWarning for this request.
            with warnings.catch_warnings():
                warnings.filterwarnings("ignore", category=InsecureRequestWarning)
                requests.get("http://127.0.0.1", verify=False)
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
    tljh_config_src = os.path.join(prefix, "bin", "tljh-config")
    tljh_config_dest = "/usr/bin/tljh-config"
    if os.path.exists(tljh_config_dest):
        if os.path.realpath(tljh_config_dest) != tljh_config_src:
            #  tljh-config exists that isn't ours. We should *not* delete this file,
            # instead we throw an error and abort. Deleting files owned by other people
            # while running as root is dangerous, especially with symlinks involved.
            raise FileExistsError(
                f"/usr/bin/tljh-config exists but is not a symlink to {tljh_config_src}"
            )
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
        conda.ensure_pip_packages(HUB_ENV_PREFIX, plugins, upgrade=True)

    # Set up plugin infrastructure
    pm = pluggy.PluginManager("tljh")
    pm.add_hookspecs(hooks)
    pm.load_setuptools_entrypoints("tljh")

    return pm


def run_plugin_actions(plugin_manager):
    """
    Run installer hooks defined in plugins
    """
    hook = plugin_manager.hook
    # Install apt packages
    apt_packages = list(set(itertools.chain(*hook.tljh_extra_apt_packages())))
    if apt_packages:
        logger.info(
            "Installing {} apt packages collected from plugins: {}".format(
                len(apt_packages), " ".join(apt_packages)
            )
        )
        apt.install_packages(apt_packages)

    # Install hub pip packages
    hub_pip_packages = list(set(itertools.chain(*hook.tljh_extra_hub_pip_packages())))
    if hub_pip_packages:
        logger.info(
            "Installing {} hub pip packages collected from plugins: {}".format(
                len(hub_pip_packages), " ".join(hub_pip_packages)
            )
        )
        conda.ensure_pip_packages(
            HUB_ENV_PREFIX,
            hub_pip_packages,
            upgrade=True,
        )

    # Install conda packages
    conda_packages = list(set(itertools.chain(*hook.tljh_extra_user_conda_packages())))
    if conda_packages:
        logger.info(
            "Installing {} user conda packages collected from plugins: {}".format(
                len(conda_packages), " ".join(conda_packages)
            )
        )
        conda.ensure_conda_packages(USER_ENV_PREFIX, conda_packages)

    # Install pip packages
    user_pip_packages = list(set(itertools.chain(*hook.tljh_extra_user_pip_packages())))
    if user_pip_packages:
        logger.info(
            "Installing {} user pip packages collected from plugins: {}".format(
                len(user_pip_packages), " ".join(user_pip_packages)
            )
        )
        conda.ensure_pip_packages(
            USER_ENV_PREFIX,
            user_pip_packages,
            upgrade=True,
        )

    # Custom post install actions
    hook.tljh_post_install()


def ensure_config_yaml(plugin_manager):
    """
    Ensure we have a config.yaml present
    """
    # ensure config dir exists and is private
    for path in [CONFIG_DIR, os.path.join(CONFIG_DIR, "jupyterhub_config.d")]:
        os.makedirs(path, mode=0o700, exist_ok=True)

    migrator.migrate_config_files()

    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE) as f:
            config = yaml.load(f)
    else:
        config = {}

    hook = plugin_manager.hook
    hook.tljh_config_post_install(config=config)

    with open(CONFIG_FILE, "w+") as f:
        yaml.dump(config, f)


def main():
    from .log import init_logging

    init_logging()

    argparser = argparse.ArgumentParser()
    argparser.add_argument(
        "--admin", nargs="*", action="append", help="List of usernames set to be admin"
    )
    argparser.add_argument(
        "--user-requirements-txt-url",
        help="URL to a requirements.txt file that should be installed in the user environment",
    )
    argparser.add_argument("--plugin", nargs="*", help="Plugin pip-specs to install")
    argparser.add_argument(
        "--progress-page-server-pid",
        type=int,
        help="The pid of the progress page server",
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


if __name__ == "__main__":
    main()
