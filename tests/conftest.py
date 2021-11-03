"""pytest fixtures"""
from importlib import reload
import os
import types
from unittest import mock

import pytest

import tljh


@pytest.fixture
def tljh_dir(tmpdir):
    """Fixture for setting up a temporary tljh dir"""
    tljh_dir = str(tmpdir.join("tljh").mkdir())
    with mock.patch.dict(os.environ, {"TLJH_INSTALL_PREFIX": tljh_dir}):
        reload(tljh)
        for name in dir(tljh):
            mod = getattr(tljh, name)
            if isinstance(mod, types.ModuleType) and mod.__name__.startswith("tljh."):
                reload(mod)
        assert tljh.config.INSTALL_PREFIX == tljh_dir
        os.makedirs(tljh.config.STATE_DIR)
        os.makedirs(tljh.config.CONFIG_DIR)
        os.makedirs(os.path.join(tljh.config.CONFIG_DIR, "traefik_config.d"))
        yield tljh_dir
