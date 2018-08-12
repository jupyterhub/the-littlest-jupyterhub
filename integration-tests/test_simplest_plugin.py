"""
Test simplest plugin
"""
from ruamel.yaml import YAML
import os
import subprocess

yaml = YAML(typ='rt')


def test_apt_packages():
    """
    Test extra apt packages are installed
    """
    assert os.path.exists('/usr/bin/sl')


def test_pip_packages():
    """
    Test extra user pip packages are installed
    """
    subprocess.check_call([
        '/opt/tljh/user/bin/python3',
        '-c',
        'import django'
    ])


def test_conda_packages():
    """
    Test extra user conda packages are installed
    """
    subprocess.check_call([
        '/opt/tljh/user/bin/python3',
        '-c',
        'import hypothesis'
    ])


def test_config_hook():
    """
    Check config changes are present
    """
    with open('/opt/tljh/config.yaml') as f:
        data = yaml.load(f)

    assert data['simplest_plugin']['present']