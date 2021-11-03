"""
Unit test  functions in installer.py
"""
import os
import pytest

from tljh import installer
from tljh.yaml import yaml


def test_ensure_config_yaml(tljh_dir):
    pm = installer.setup_plugins()
    installer.ensure_config_yaml(pm)
    assert os.path.exists(installer.CONFIG_FILE)
    assert os.path.isdir(installer.CONFIG_DIR)
    assert os.path.isdir(os.path.join(installer.CONFIG_DIR, "jupyterhub_config.d"))
    # verify that old config doesn't exist
    assert not os.path.exists(os.path.join(tljh_dir, "config.yaml"))


@pytest.mark.parametrize(
    "admins, expected_config",
    [
        ([["a1"], ["a2"], ["a3"]], ["a1", "a2", "a3"]),
        ([["a1:p1"], ["a2"]], ["a1", "a2"]),
    ],
)
def test_ensure_admins(tljh_dir, admins, expected_config):
    # --admin option called multiple times on the installer
    # creates a list of argument lists.
    installer.ensure_admins(admins)

    config_path = installer.CONFIG_FILE
    with open(config_path) as f:
        config = yaml.load(f)

    # verify the list was flattened
    assert config["users"]["admin"] == expected_config
