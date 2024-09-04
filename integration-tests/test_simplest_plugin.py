"""
Test the plugin in integration-tests/plugins/simplest that makes use of all tljh
recognized plugin hooks that are defined in tljh/hooks.py.
"""

import os
import subprocess

from ruamel.yaml import YAML

from tljh import user
from tljh.config import CONFIG_FILE, HUB_ENV_PREFIX, USER_ENV_PREFIX

GIT_REPO_PATH = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
yaml = YAML(typ="rt")


def test_tljh_extra_user_conda_packages():
    subprocess.check_call([f"{USER_ENV_PREFIX}/bin/python3", "-c", "import tqdm"])


def test_tljh_extra_user_pip_packages():
    subprocess.check_call([f"{USER_ENV_PREFIX}/bin/python3", "-c", "import simplejson"])


def test_tljh_extra_hub_pip_packages():
    subprocess.check_call([f"{HUB_ENV_PREFIX}/bin/python3", "-c", "import there"])


def test_conda_packages():
    """
    Test extra user conda packages are installed from multiple channels.

    - tqdm installs from the conda-forge channel (https://conda-forge.org/packages/)
    - csvtk installs from the bioconda channel (https://bioconda.github.io/conda-package_index.html)
    """
    subprocess.check_call([f"{USER_ENV_PREFIX}/bin/python3", "-c", "import tqdm"])
    subprocess.check_call([f"{USER_ENV_PREFIX}/bin/csvtk", "cat", "--help"])


def test_tljh_extra_apt_packages():
    assert os.path.exists("/usr/games/sl")


def test_tljh_custom_jupyterhub_config():
    """
    Test that the provided tljh_custom_jupyterhub_config hook has made the tljh
    jupyterhub load additional jupyterhub config.
    """
    tljh_jupyterhub_config = os.path.join(GIT_REPO_PATH, "tljh", "jupyterhub_config.py")
    output = subprocess.check_output(
        [
            f"{HUB_ENV_PREFIX}/bin/python3",
            "-m",
            "jupyterhub",
            "--show-config",
            "--config",
            tljh_jupyterhub_config,
        ],
        text=True,
    )
    assert "jupyterhub_config_set_by_simplest_plugin" in output


def test_tljh_config_post_install():
    """
    Test that the provided tljh_config_post_install hook has made tljh recognize
    additional tljh config.
    """
    with open(CONFIG_FILE) as f:
        tljh_config = yaml.load(f)
    assert tljh_config["Test"]["tljh_config_set_by_simplest_plugin"]


def test_tljh_post_install():
    """
    Test that the provided tljh_post_install hook has been executed by looking
    for a specific file written.
    """
    with open("test_tljh_post_install") as f:
        content = f.read()
    assert "file_written_by_simplest_plugin" in content


def test_tljh_new_user_create():
    """
    Test that the provided tljh_new_user_create hook has been executed by
    looking for a specific file written.
    """
    # Trigger the hook by letting tljh's code create a user
    username = "user1"
    user.ensure_user(username)

    with open("test_new_user_create") as f:
        content = f.read()
    assert "file_written_by_simplest_plugin" in content
    assert username in content
