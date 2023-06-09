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

from tljh import apt, conda, hooks, migrator, systemd, traefik, user

from .config import (
    CONFIG_DIR,
    CONFIG_FILE,
    HUB_ENV_PREFIX,
    INSTALL_PREFIX,
    STATE_DIR,
    USER_ENV_PREFIX,
)
from .utils import parse_version as V
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
    # Install dependencies for installing pycurl via pip, where build-essential
    # is generally useful for installing other packages as well.
    apt.install_packages(["libssl-dev", "libcurl4-openssl-dev", "build-essential"])

    conda.ensure_pip_requirements(
        prefix,
        os.path.join(HERE, "requirements-hub-env.txt"),
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
    os.makedirs("/etc/sudoers.d/", exist_ok=True)
    with open("/etc/sudoers.d/jupyterhub-admins", "w") as f:
        # JupyterHub admins should have full passwordless sudo access
        f.write("%jupyterhub-admins ALL = (ALL) NOPASSWD: ALL\n")
        # `sudo -E` should preserve the $PATH we set. This allows
        # admins in jupyter terminals to do `sudo -E pip install <package>`,
        # `pip` is in the $PATH we set in jupyterhub_config.py to include the user conda env.
        f.write("Defaults exempt_group = jupyterhub-admins\n")


# Install mambaforge using an installer from
# https://github.com/conda-forge/miniforge/releases
MAMBAFORGE_VERSION = "23.1.0-1"
# sha256 checksums
MAMBAFORGE_CHECKSUMS = {
    "aarch64": "d9d89c9e349369702171008d9ee7c5ce80ed420e5af60bd150a3db4bf674443a",
    "x86_64": "cfb16c47dc2d115c8b114280aa605e322173f029fdb847a45348bf4bd23c62ab",
}

# minimum versions of packages
MINIMUM_VERSIONS = {
    # if conda/mamba/pip are lower than this, upgrade them before installing the user packages
    "mamba": "1.4.2",
    "conda": "23.3.1",
    "pip": "23.1.2",
    # minimum Python version (if not matched, abort to avoid big disruptive updates)
    "python": "3.9",
}


def _mambaforge_url(version=MAMBAFORGE_VERSION, arch=None):
    """Return (URL, checksum) for mambaforge download for a given version and arch

    Default values provided for both version and arch
    """
    if arch is None:
        arch = os.uname().machine
    installer_url = "https://github.com/conda-forge/miniforge/releases/download/{v}/Mambaforge-{v}-Linux-{arch}.sh".format(
        v=version,
        arch=arch,
    )
    # Check system architecture, set appropriate installer checksum
    checksum = MAMBAFORGE_CHECKSUMS.get(arch)
    if not checksum:
        raise ValueError(
            f"Unsupported architecture: {arch}. TLJH only supports {','.join(MAMBAFORGE_CHECKSUMS.keys())}"
        )
    return installer_url, checksum


def ensure_user_environment(user_requirements_txt_file):
    """
    Set up user conda environment with required packages
    """
    logger.info("Setting up user environment...")
    # Check OS, set appropriate string for conda installer path
    if os.uname().sysname != "Linux":
        raise OSError("TLJH is only supported on Linux platforms.")

    # Check the existing environment for what to do
    package_versions = conda.get_conda_package_versions(USER_ENV_PREFIX)
    is_fresh_install = not package_versions

    if is_fresh_install:
        # If no Python environment is detected but a folder exists we abort to
        # avoid clobbering something we don't recognize.
        if os.path.exists(USER_ENV_PREFIX) and os.listdir(USER_ENV_PREFIX):
            msg = f"Found non-empty directory that is not a conda install in {USER_ENV_PREFIX}. Please remove it (or rename it to preserve files) and run tljh again."
            logger.error(msg)
            raise OSError(msg)

        logger.info("Downloading & setting up user environment...")
        installer_url, installer_sha256 = _mambaforge_url()
        with conda.download_miniconda_installer(
            installer_url, installer_sha256
        ) as installer_path:
            conda.install_miniconda(installer_path, USER_ENV_PREFIX)
        package_versions = conda.get_conda_package_versions(USER_ENV_PREFIX)

        # quick sanity check: we should have conda and mamba!
        assert "conda" in package_versions
        assert "mamba" in package_versions

    # Check Python version
    python_version = package_versions["python"]
    logger.debug(f"Found python={python_version} in {USER_ENV_PREFIX}")
    if V(python_version) < V(MINIMUM_VERSIONS["python"]):
        msg = (
            f"TLJH requires Python >={MINIMUM_VERSIONS['python']}, found python={python_version} in {USER_ENV_PREFIX}."
            f"\nPlease upgrade Python (may be highly disruptive!), or remove/rename {USER_ENV_PREFIX} to allow TLJH to make a fresh install."
            f"\nYou can use `{USER_ENV_PREFIX}/bin/conda list` to save your current list of packages."
        )
        logger.error(msg)
        raise ValueError(msg)

    # Ensure minimum versions of the following packages by upgrading to the
    # latest if below that version.
    #
    # - conda/mamba, via conda-forge
    # - pip,         via PyPI
    #
    to_upgrade = []
    for pkg in ("conda", "mamba", "pip"):
        version = package_versions.get(pkg)
        min_version = MINIMUM_VERSIONS[pkg]
        if not version:
            logger.warning(f"{USER_ENV_PREFIX} is missing {pkg}, installing it...")
            to_upgrade.append(pkg)
        else:
            logger.debug(f"Found {pkg}=={version} in {USER_ENV_PREFIX}")
            if V(version) < V(min_version):
                logger.info(
                    f"{USER_ENV_PREFIX} has {pkg}=={version}, it will be upgraded to {pkg}>={min_version}"
                )
                to_upgrade.append(pkg)

        cf_pkgs_to_upgrade = list(set(to_upgrade) & {"conda", "mamba"})
        if cf_pkgs_to_upgrade:
            conda.ensure_conda_packages(
                USER_ENV_PREFIX,
                # we _could_ explicitly pin Python here,
                # but conda already does this by default
                cf_pkgs_to_upgrade,
            )
        pypi_pkgs_to_upgrade = list(set(to_upgrade) & {"pip"})
        if pypi_pkgs_to_upgrade:
            conda.ensure_pip_packages(
                USER_ENV_PREFIX,
                pypi_pkgs_to_upgrade,
                upgrade=True,
            )

    # Install/upgrade the jupyterhub version in the user env based on the
    # version specification used for the hub env.
    #
    with open(os.path.join(HERE, "requirements-hub-env.txt")) as f:
        jh_version_spec = [l for l in f if l.startswith("jupyterhub>=")][0]
    conda.ensure_pip_packages(USER_ENV_PREFIX, [jh_version_spec], upgrade=True)

    # Install user environment extras for initial installations
    #
    if is_fresh_install:
        conda.ensure_pip_requirements(
            USER_ENV_PREFIX,
            os.path.join(HERE, "requirements-user-env-extras.txt"),
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
    Setup given list of user[:password] strings as admins.
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
    if args.user_requirements_txt_url:
        logger.info("installing packages from user_requirements_txt_url")
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

    ensure_jupyterhub_service(HUB_ENV_PREFIX)
    ensure_jupyterhub_running()
    ensure_symlinks(HUB_ENV_PREFIX)

    # Run installer plugins last
    run_plugin_actions(pm)

    logger.info("Done!")


if __name__ == "__main__":
    main()
