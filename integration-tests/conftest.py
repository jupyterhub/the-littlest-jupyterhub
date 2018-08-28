"""pytest fixtures"""

import os

from pytest import fixture

from tljh.config import CONFIG_FILE, reload_component


@fixture
def preserve_config(request):
    """Fixture to save and restore config around tests"""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE) as f:
            save_config = f.read()
    else:
        save_config = None
    try:
        yield
    finally:
        if save_config:
            with open(CONFIG_FILE, "w") as f:
                f.write(save_config)
        elif os.path.exists(CONFIG_FILE):
            os.remove(CONFIG_FILE)
        reload_component("hub")
        reload_component("proxy")
