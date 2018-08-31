"""
Unit test  functions in installer.py
"""
import os
from datetime import date

from tljh import migrator, config


def test_migrate_config(tljh_dir):
    CONFIG_FILE = config.CONFIG_FILE
    CONFIG_DIR = config.CONFIG_DIR
    OLD_CONFIG_FILE = os.path.join(tljh_dir, "config.yaml")
    OLD_CONFIG_D = os.path.join(tljh_dir, "jupyterhub_config.d")
    CONFIG_D = os.path.join(config.CONFIG_DIR, "jupyterhub_config.d")
    old_config_py = os.path.join(OLD_CONFIG_D, "upgrade.py")
    new_config_py = os.path.join(CONFIG_D, "upgrade.py")

    # initial condition: nothing exists
    assert not os.path.exists(CONFIG_FILE)
    assert not os.path.exists(OLD_CONFIG_FILE)
    assert os.path.isdir(CONFIG_DIR)

    # run migration with old config and no new config
    upgraded_config = "old: config\n"
    with open(OLD_CONFIG_FILE, "w") as f:
        f.write(upgraded_config)
    os.makedirs(OLD_CONFIG_D, exist_ok=True)
    with open(old_config_py, "w") as f:
        f.write("c.JupyterHub.log_level = 10")

    migrator.migrate_config_files()
    assert os.path.exists(CONFIG_FILE)
    assert not os.path.exists(OLD_CONFIG_FILE)
    with open(CONFIG_FILE) as f:
        assert f.read() == upgraded_config
    assert os.path.exists(new_config_py)
    assert not os.path.exists(OLD_CONFIG_D)

    # run again, this time with both old and new config
    duplicate_config = "dupe: config\n"
    with open(OLD_CONFIG_FILE, "w") as f:
        f.write(duplicate_config)
    migrator.migrate_config_files()
    assert os.path.exists(CONFIG_FILE)
    assert not os.path.exists(OLD_CONFIG_FILE)
    # didn't clobber config:
    with open(CONFIG_FILE) as f:
        assert f.read() == upgraded_config

    # preserved old config
    backup_config = CONFIG_FILE + f".old.{date.today().isoformat()}"
    assert os.path.exists(backup_config)
    with open(backup_config) as f:
        assert f.read() == duplicate_config

    # migrate jupyterhub_con
