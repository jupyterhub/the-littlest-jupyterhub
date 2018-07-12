"""
Parse YAML config file & update JupyterHub config.

Config should never append or mutate, only set. Functions here could
be called many times per lifetime of a jupyterhub.

Traitlets that modify the startup of JupyterHub should not be here.
FIXME: A strong feeling that JSON Schema should be involved somehow.
"""
import copy
import os
import yaml

# Default configuration for tljh
# User provided config is merged into this
default = {
    'auth': {
        'type': 'firstuse',
        'dummy': {},
        'firstuse': {
            'createUsers': False
        }
    },
    'users': {
        'allowed': [],
        'banned': [],
        'admin': []
    },
    'limits': {
        'memory': '1G',
        'cpu': None
    },
    'userEnvironment': {
        'defaultApp': 'classic'
    }

}


def apply_yaml_config(path, c):
    if os.path.exists(path):
        with open(path) as f:
            # FIXME: Figure out correct order of merging here
            tljh_config = _merge_dictionaries(dict(default), yaml.safe_load(f))
    else:
        tljh_config = copy.deepcopy(default)

    update_auth(c, tljh_config)
    update_userlists(c, tljh_config)
    update_limits(c, tljh_config)
    update_user_environment(c, tljh_config)
    update_user_account_config(c, tljh_config)


def update_auth(c, config):
    """
    Set auth related configuration from YAML config file
    """
    auth = config.get('auth')

    if auth['type'] == 'dummy':
        c.JupyterHub.authenticator_class = 'dummyauthenticator.DummyAuthenticator'
        password = auth['dummy'].get('password')
        if password is not None:
            c.DummyAuthenticator.password = password
        return
    elif auth['type'] == 'firstuse':
        c.JupyterHub.authenticator_class = 'firstuseauthenticator.FirstUseAuthenticator'
        c.FirstUseAuthenticator.create_users = auth['firstuse']['createUsers']


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
    user_env = config['userEnvironment']

    # Set default application users are launched into
    if user_env['defaultApp'] == 'jupyterlab':
        c.Spawner.default_url = '/lab'
    elif user_env['defaultApp'] == 'nteract':
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
