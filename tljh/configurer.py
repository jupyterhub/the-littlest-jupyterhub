"""
Parse YAML config file & update JupyterHub config.

Config should never append or mutate, only set. Functions here could
be called many times per lifetime of a jupyterhub.

Traitlets that modify the startup of JupyterHub should not be here.
FIXME: A strong feeling that JSON Schema should be involved somehow.
"""

import os
import yaml

from tljh.config import CONFIG_FILE

# Default configuration for tljh
# User provided config is merged into this
default = {
    'auth': {
        'type': 'nativeauthenticator.NativeAuthenticator',
        'NativeAuthenticator': {}
    },
    'users': {
        'allowed': [],
        'banned': [],
        'admin': [],
    },
    'limits': {
        'memory': None,
        'cpu': None,
    },
    'http': {
        'port': 80,
    },
    'https': {
        'enabled': False,
        'port': 443,
        'tls': {
            'cert': '',
            'key': '',
        },
        'letsencrypt': {
            'email': '',
            'domains': [],
        },
    },
    'user_environment': {
        'default_app': 'classic',
    },
}


def load_config(config_file=CONFIG_FILE):
    """Load the current config as a dictionary

    merges overrides from config.yaml with default config
    """
    if os.path.exists(config_file):
        with open(config_file) as f:
            config_overrides = yaml.safe_load(f)
    else:
        config_overrides = {}
    return _merge_dictionaries(dict(default), config_overrides)


def apply_config(config_overrides, c):
    """
    Merge config_overrides with config defaults & apply to JupyterHub config c
    """
    tljh_config = _merge_dictionaries(dict(default), config_overrides)

    update_auth(c, tljh_config)
    update_userlists(c, tljh_config)
    update_limits(c, tljh_config)
    update_user_environment(c, tljh_config)
    update_user_account_config(c, tljh_config)


def set_if_not_none(parent, key, value):
    """
    Set attribute 'key' on parent if value is not None
    """
    if value is not None:
        setattr(parent, key, value)


def update_auth(c, config):
    """
    Set auth related configuration from YAML config file

    Use auth.type to determine authenticator to use. All parameters
    in the config under auth.{auth.type} will be passed straight to the
    authenticators themselves.
    """
    auth = config.get('auth')

    # FIXME: Make sure this is something importable.
    # FIXME: SECURITY: Class must inherit from Authenticator, to prevent us being
    # used to set arbitrary properties on arbitrary types of objects!
    authenticator_class = auth['type']
    # When specifying fully qualified name, use classname as key for config
    authenticator_configname = authenticator_class.split('.')[-1]
    c.JupyterHub.authenticator_class = authenticator_class
    # Use just class name when setting config. If authenticator is dummyauthenticator.DummyAuthenticator,
    # its config will be set under c.DummyAuthenticator
    authenticator_parent = getattr(c, authenticator_class.split('.')[-1])

    for k, v in auth.get(authenticator_configname, {}).items():
        set_if_not_none(authenticator_parent, k, v)


def update_userlists(c, config):
    """
    Set user whitelists & admin lists
    """
    users = config['users']

    c.Authenticator.whitelist = set(users['allowed'])
    c.Authenticator.blacklist = set(users['banned'])
    c.Authenticator.admin_users = set(users['admin'])


def update_limits(c, config):
    """
    Set user server limits
    """
    limits = config['limits']

    c.SystemdSpawner.mem_limit = limits['memory']
    c.SystemdSpawner.cpu_limit = limits['cpu']


def update_user_environment(c, config):
    """
    Set user environment configuration
    """
    user_env = config['user_environment']

    # Set default application users are launched into
    if user_env['default_app'] == 'jupyterlab':
        c.Spawner.default_url = '/lab'
    elif user_env['default_app'] == 'nteract':
        c.Spawner.default_url = '/nteract'


def update_user_account_config(c, config):
    c.SystemdSpawner.username_template = 'jupyter-{USERNAME}'


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
                raise Exception('Conflict at %s' % '.'.join(path + [str(key)]))
        else:
            a[key] = b[key]
    return a
