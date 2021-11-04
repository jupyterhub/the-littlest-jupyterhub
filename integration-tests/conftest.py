"""pytest fixtures"""

import os

from pytest import fixture


@fixture
def preserve_config(request):
    """Fixture to save and restore config around tests"""
    # Import TLJH only when needed. This lets us run tests in places
    # where TLJH is not installed - particularly, the 'distro check' test.
    from tljh.config import CONFIG_FILE, reload_component

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
