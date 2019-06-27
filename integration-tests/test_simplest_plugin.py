"""
Test simplest plugin
"""
from ruamel.yaml import YAML
import requests
import os
import subprocess
from tljh.config import CONFIG_FILE, USER_ENV_PREFIX, HUB_ENV_PREFIX
from tljh.systemd import check_service_enabled

yaml = YAML(typ='rt')


def test_apt_packages():
    """
    Test extra apt packages are installed
    """
    assert os.path.exists('/usr/games/sl')


def test_pip_packages():
    """
    Test extra user & hub pip packages are installed
    """
    subprocess.check_call([
        f'{USER_ENV_PREFIX}/bin/python3',
        '-c',
        'import django'
    ])

    subprocess.check_call([
        f'{HUB_ENV_PREFIX}/bin/python3',
        '-c',
        'import there'
    ])


def test_conda_packages():
    """
    Test extra user conda packages are installed
    """
    subprocess.check_call([
        f'{USER_ENV_PREFIX}/bin/python3',
        '-c',
        'import hypothesis'
    ])


def test_config_hook():
    """
    Check config changes are present
    """
    with open(CONFIG_FILE) as f:
        data = yaml.load(f)

    assert data['simplest_plugin']['present']


def test_jupyterhub_config_hook():
    """
    Test that tmpauthenticator is enabled by our custom config plugin
    """
    resp = requests.get('http://localhost/hub/tmplogin', allow_redirects=False)
    assert resp.status_code == 302
    assert resp.headers['Location'] == '/hub/spawn'


def test_post_install_hook():
    """
    Test that the post-install-test systemd service is enabled
    """
    assert check_service_enabled("post-install-test")
