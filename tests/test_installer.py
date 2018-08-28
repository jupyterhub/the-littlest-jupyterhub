"""
Unit test  functions in installer.py
"""
import os
from datetime import date

from tljh import installer



def test_ensure_node():
    installer.ensure_node()
    assert os.path.exists('/usr/bin/node')


def test_ensure_config_yaml(tljh_dir):
    pm = installer.setup_plugins()
    installer.ensure_config_yaml(pm)
    assert os.path.exists(installer.CONFIG_FILE)
    assert os.path.isdir(installer.CONFIG_DIR)
    assert os.path.isdir(os.path.join(installer.CONFIG_DIR, 'jupyterhub_config.d'))
    assert not os.path.exists(installer.OLD_CONFIG_FILE)

    # run again, with old config in the way and no new config
    upgraded_config = 'old: config\n'
    with open(installer.OLD_CONFIG_FILE, 'w') as f:
        f.write(upgraded_config)
    os.remove(installer.CONFIG_FILE)
    installer.ensure_config_yaml(pm)
    assert os.path.exists(installer.CONFIG_FILE)
    assert not os.path.exists(installer.OLD_CONFIG_FILE)
    with open(installer.CONFIG_FILE) as f:
        assert f.read() == upgraded_config

    # run again, this time with both old and new config
    duplicate_config = 'dupe: config\n'
    with open(installer.OLD_CONFIG_FILE, 'w') as f:
        f.write(duplicate_config)
    installer.ensure_config_yaml(pm)
    assert os.path.exists(installer.CONFIG_FILE)
    assert not os.path.exists(installer.OLD_CONFIG_FILE)
    # didn't clobber config:
    with open(installer.CONFIG_FILE) as f:
        assert f.read() == upgraded_config

    # preserved old config
    backup_config = installer.CONFIG_FILE + f".old.{date.today().isoformat()}"
    assert os.path.exists(backup_config)
    with open(backup_config) as f:
        assert f.read() == duplicate_config







