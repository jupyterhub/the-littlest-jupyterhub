"""
Test simplest plugin
"""
from ruamel.yaml import YAML
import os
import subprocess
from tljh.config import CONFIG_FILE, USER_ENV_PREFIX

yaml = YAML(typ='rt')


def test_apt_packages():
    """
    Test extra apt packages are installed
    """
    assert os.path.exists('/usr/games/sl')


def test_pip_packages():
    """
    Test extra user pip packages are installed
    """
    subprocess.check_call([
        f'{USER_ENV_PREFIX}/bin/python3',
        '-c',
        'import django'
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
