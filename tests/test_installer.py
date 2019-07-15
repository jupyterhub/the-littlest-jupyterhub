"""
Unit test  functions in installer.py
"""
import os

from tljh import installer
from tljh.yaml import yaml


def test_ensure_node():
    installer.ensure_node()
    assert os.path.exists('/usr/bin/node')


def test_ensure_config_yaml(tljh_dir):
    pm = installer.setup_plugins()
    installer.ensure_config_yaml(pm)
    assert os.path.exists(installer.CONFIG_FILE)
    assert os.path.isdir(installer.CONFIG_DIR)
    assert os.path.isdir(os.path.join(installer.CONFIG_DIR, 'jupyterhub_config.d'))
    # verify that old config doesn't exist
    assert not os.path.exists(os.path.join(tljh_dir, 'config.yaml'))

def test_ensure_admins(tljh_dir):
	# --admin option called multiple times on the installer
	# creates a list of argument lists.
	admins = [['a1'], ['a2'], ['a3']]
	installer.ensure_admins(admins)

	config_path = installer.CONFIG_FILE
	with open(config_path, 'r') as f:
	    config = yaml.load(f)

	# verify the list was flattened
	assert config['users']['admin'] == ['a1', 'a2', 'a3']
