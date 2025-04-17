"""
Parse YAML config file & update JupyterHub config.

Config should never append or mutate, only set. Functions here could
be called many times per lifetime of a jupyterhub.

Traitlets that modify the startup of JupyterHub should not be here.
"""

import os
import sys

from .config import CONFIG_FILE, STATE_DIR
from .yaml import yaml

# Default configuration for tljh
# User provided config is merged into this
default = {
    "base_url": "/",
    "auth": {
        "type": "firstuseauthenticator.FirstUseAuthenticator",
        "FirstUseAuthenticator": {"create_users": False},
    },
    "users": {"allowed": [], "banned": [], "admin": [], "extra_user_groups": {}},
    "limits": {
        "memory": None,
        "cpu": None,
    },
    "http": {
        "address": "",
        "port": 80,
    },
    "https": {
        "enabled": False,
        "address": "",
        "port": 443,
        "tls": {
            "cert": "",
            "key": "",
        },
        "letsencrypt": {
            "email": "",
            "domains": [],
            "staging": False,
        },
    },
    "traefik_api": {
        "ip": "127.0.0.1",
        "port": 8099,
        "username": "api_admin",
        "password": "",
    },
    "user_environment": {
        "default_app": "jupyterlab",
    },
    "services": {
        "cull": {
            "enabled": True,
            "timeout": 600,
            "every": 60,
            "concurrency": 5,
            "users": False,
            "max_age": 0,
            "remove_named_servers": False,
        },
    },
}


def load_config(config_file=CONFIG_FILE):
    """Load the current config as a dictionary

    merges overrides from config.yaml with default config
    """
    if os.path.exists(config_file):
        with open(config_file) as f:
            config_overrides = yaml.load(f)
    else:
        config_overrides = {}

    secrets = load_secrets()
    config = _merge_dictionaries(dict(default), secrets)
    config = _merge_dictionaries(config, config_overrides)
    return config


def apply_config(config_overrides, c):
    """
    Merge config_overrides with config defaults & apply to JupyterHub config c
    """
    tljh_config = _merge_dictionaries(dict(default), config_overrides)

    update_base_url(c, tljh_config)
    update_auth(c, tljh_config)
    update_userlists(c, tljh_config)
    update_usergroups(c, tljh_config)
    update_limits(c, tljh_config)
    update_user_environment(c, tljh_config)
    update_user_account_config(c, tljh_config)
    update_traefik_api(c, tljh_config)
    update_services(c, tljh_config)


def set_if_not_none(parent, key, value):
    """
    Set attribute 'key' on parent if value is not None
    """
    if value is not None:
        setattr(parent, key, value)


def load_traefik_api_credentials():
    """Load traefik api secret from a file"""
    proxy_secret_path = os.path.join(STATE_DIR, "traefik-api.secret")
    if not os.path.exists(proxy_secret_path):
        return {}
    with open(proxy_secret_path) as f:
        password = f.read()
    return {
        "traefik_api": {
            "password": password,
        }
    }


def load_secrets():
    """Load any secret values stored on disk

    Returns dict to be merged into config during load
    """
    config = {}
    config = _merge_dictionaries(config, load_traefik_api_credentials())
    return config


def update_base_url(c, config):
    """
    Update base_url of JupyterHub through tljh config
    """
    c.JupyterHub.base_url = config["base_url"]


def update_auth(c, config):
    """
    Set auth related configuration from YAML config file.

    As an example, this function should update the following TLJH auth
    configuration:

    ```yaml
    auth:
      type: oauthenticator.github.GitHubOAuthenticator
      GitHubOAuthenticator:
        client_id: "..."
        client_secret: "..."
        oauth_callback_url: "..."
      ArbitraryClass:
        arbitrary_key: "..."
        arbitrary_key_with_none_value:
    ```

    by applying the following configuration:

    ```python
    c.JupyterHub.authenticator_class = "oauthenticator.github.GitHubOAuthenticator"
    c.GitHubOAuthenticator.client_id = "..."
    c.GitHubOAuthenticator.client_secret = "..."
    c.GitHubOAuthenticator.oauth_callback_url = "..."
    c.ArbitraryClass.arbitrary_key = "..."
    ```

    Note that "auth.type" and "auth.ArbitraryClass.arbitrary_key_with_none_value"
    are treated a bit differently. auth.type will always map to
    c.JupyterHub.authenticator_class and any configured value being None won't
    be set.
    """
    tljh_auth_config = config["auth"]

    c.JupyterHub.authenticator_class = tljh_auth_config["type"]

    for auth_key, auth_value in tljh_auth_config.items():
        if not (auth_key[0] == auth_key[0].upper() and isinstance(auth_value, dict)):
            if auth_key == "type":
                continue
            raise ValueError(
                f"Error: auth.{auth_key} was ignored, it didn't look like a valid configuration"
            )
        class_name = auth_key
        class_config_to_set = auth_value
        class_config = c[class_name]
        for config_name, config_value in class_config_to_set.items():
            set_if_not_none(class_config, config_name, config_value)


def update_userlists(c, config):
    """
    Set user whitelists & admin lists
    """
    users = config["users"]

    if (
        not users["allowed"]
        and config["auth"]["type"] == default["auth"]["type"]
        and "allow_all" not in c.FirstUseAuthenticator
    ):
        # _default_ authenticator, enable allow_all if no users specified
        c.FirstUseAuthenticator.allow_all = True

    c.Authenticator.allowed_users = set(users["allowed"])
    c.Authenticator.blocked_users = set(users["banned"])
    c.Authenticator.admin_users = set(users["admin"])


def update_usergroups(c, config):
    """
    Set user groups
    """
    users = config["users"]
    c.UserCreatingSpawner.user_groups = users["extra_user_groups"]


def update_limits(c, config):
    """
    Set user server limits
    """
    limits = config["limits"]

    c.Spawner.mem_limit = limits["memory"]
    c.Spawner.cpu_limit = limits["cpu"]


def update_user_environment(c, config):
    """
    Set user environment configuration
    """
    user_env = config["user_environment"]

    # Set default application users are launched into
    if user_env["default_app"] == "jupyterlab":
        c.Spawner.default_url = "/lab"
    elif user_env["default_app"] == "classic":
        c.Spawner.default_url = "/tree"


def update_user_account_config(c, config):
    c.SystemdSpawner.username_template = "jupyter-{USERNAME}"


def update_traefik_api(c, config):
    """
    Set traefik api endpoint credentials
    """
    c.TraefikProxy.traefik_api_username = config["traefik_api"]["username"]
    c.TraefikProxy.traefik_api_password = config["traefik_api"]["password"]
    https = config["https"]
    if https["enabled"]:
        c.TraefikProxy.traefik_entrypoint = "https"
    else:
        c.TraefikProxy.traefik_entrypoint = "http"


def set_cull_idle_service(config):
    """
    Set Idle Culler service
    """
    cull_cmd = [sys.executable, "-m", "jupyterhub_idle_culler"]
    cull_config = config["services"]["cull"]
    print()

    cull_cmd += ["--timeout=%d" % cull_config["timeout"]]
    cull_cmd += ["--cull-every=%d" % cull_config["every"]]
    cull_cmd += ["--concurrency=%d" % cull_config["concurrency"]]
    cull_cmd += ["--max-age=%d" % cull_config["max_age"]]
    if cull_config["users"]:
        cull_cmd += ["--cull-users"]
    if cull_config["remove_named_servers"]:
        cull_cmd += ["--remove-named-servers"]

    cull_service = {
        "name": "cull-idle",
        "admin": True,
        "command": cull_cmd,
    }

    return cull_service


def update_services(c, config):
    c.JupyterHub.services = []

    if config["services"]["cull"]["enabled"]:
        c.JupyterHub.services.append(set_cull_idle_service(config))


def _merge_dictionaries(a, b, path=None, update=True):
    """
    Merge two dictionaries recursively.

    From https://stackoverflow.com/a/7205107
    """
    if path is None:
        path = []
    for key in b:
        if key in a:
            if isinstance(a[key], dict) and isinstance(b[key], dict):
                _merge_dictionaries(a[key], b[key], path + [str(key)])
            elif a[key] == b[key]:
                pass  # same leaf value
            elif update:
                a[key] = b[key]
            else:
                raise Exception("Conflict at %s" % ".".join(path + [str(key)]))
        else:
            a[key] = b[key]
    return a
