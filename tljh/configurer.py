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
        'type': 'dummy',
        'dummy': {}
    },
    'users': {
        'allowed': [],
        'banned': [],
        'admin': []
    }
}


def apply_yaml_config(path, c):
    if not os.path.exists(path):
        user_config = copy.deepcopy(default)

    with open(path) as f:
        user_config = _merge_dictionaries(yaml.safe_load(f), default)

    update_auth(c, user_config)
    update_userlists(c, user_config)


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


def update_userlists(c, config):
    """
    Set user whitelists & admin lists
    """
    users = config['users']

    c.Authenticator.whitelist = set(users['allowed'])
    c.Authenticator.blacklist = set(users['banned'])
    c.Authenticator.admin_users = set(users['admin'])


def _merge_dictionaries(a, b, path=None, update=True):
    """
    Merge two dictionaries recursively.

    From https://stackoverflow.com/a/25270947
    """
    if path is None:
        path = []
    for key in b:
        if key in a:
            if isinstance(a[key], dict) and isinstance(b[key], dict):
                _merge_dictionaries(a[key], b[key], path + [str(key)])
            elif a[key] == b[key]:
                pass  # same leaf value
            elif isinstance(a[key], list) and isinstance(b[key], list):
                for idx, val in enumerate(b[key]):
                    a[key][idx] = _merge_dictionaries(
                        a[key][idx],
                        b[key][idx],
                        path + [str(key), str(idx)],
                        update=update
                    )
            elif update:
                a[key] = b[key]
            else:
                raise Exception('Conflict at %s' % '.'.join(path + [str(key)]))
        else:
            a[key] = b[key]
    return a
