"""
Test simplest plugin
"""
from ruamel.yaml import YAML
import requests
import os
import subprocess

from tljh.config import CONFIG_FILE, USER_ENV_PREFIX, HUB_ENV_PREFIX
from tljh import user

yaml = YAML(typ="rt")


def test_apt_packages():
    """
    Test extra apt packages are installed
    """
    assert os.path.exists("/usr/games/sl")


def test_pip_packages():
    """
    Test extra user & hub pip packages are installed
    """
    subprocess.check_call([f"{USER_ENV_PREFIX}/bin/python3", "-c", "import django"])

    subprocess.check_call([f"{HUB_ENV_PREFIX}/bin/python3", "-c", "import there"])


def test_conda_packages():
    """
    Test extra user conda packages are installed
    """
    subprocess.check_call([f"{USER_ENV_PREFIX}/bin/python3", "-c", "import hypothesis"])


def test_config_hook():
    """
    Check config changes are present
    """
    with open(CONFIG_FILE) as f:
        data = yaml.load(f)

    assert data["simplest_plugin"]["present"]


def test_jupyterhub_config_hook():
    """
    Test that tmpauthenticator is enabled by our custom config plugin
    """
    resp = requests.get("http://localhost/hub/tmplogin", allow_redirects=False)
    assert resp.status_code == 302
    assert resp.headers["Location"] == "/hub/spawn"


def test_post_install_hook():
    """
    Test that the test_post_install file has the correct content
    """
    with open("test_post_install") as f:
        content = f.read()

    assert content == "123456789"


def test_new_user_create():
    """
    Test that plugin receives username as arg
    """
    username = "user1"
    # Call ensure_user to make sure the user plugin gets called
    user.ensure_user(username)

    with open("test_new_user_create") as f:
        content = f.read()

    assert content == username
