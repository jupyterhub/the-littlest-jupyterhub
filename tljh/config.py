"""
Commandline interface for setting config items in config.yaml.

Used as:

tljh-config set firstlevel.second_level something

tljh-config show

tljh-config show firstlevel

tljh-config show firstlevel.second_level
"""

import argparse
from collections import Sequence, Mapping
from copy import deepcopy
import os
import re
import sys

from .yaml import yaml


INSTALL_PREFIX = os.environ.get('TLJH_INSTALL_PREFIX', '/opt/tljh')
HUB_ENV_PREFIX = os.path.join(INSTALL_PREFIX, 'hub')
USER_ENV_PREFIX = os.path.join(INSTALL_PREFIX, 'user')
STATE_DIR = os.path.join(INSTALL_PREFIX, 'state')
CONFIG_DIR = os.path.join(INSTALL_PREFIX, 'config')
CONFIG_FILE = os.path.join(CONFIG_DIR, 'config.yaml')


def set_item_in_config(config, property_path, value):
    """
    Set key at property_path to value in config & return new config.

    config is not mutated.

    property_path is a series of dot separated values. Any part of the path
    that does not exist is created.
    """
    path_components = property_path.split('.')

    # Mutate a copy of the config, not config itself
    cur_part = config_copy = deepcopy(config)
    for i, cur_path in enumerate(path_components):
        cur_path = path_components[i]
        if i == len(path_components) - 1:
            # Final component
            cur_part[cur_path] = value
        else:
            # If we are asked to create new non-leaf nodes, we will always make them dicts
            # This means setting is *destructive* - will replace whatever is down there!
            if cur_path not in cur_part or not _is_dict(cur_part[cur_path]):
                cur_part[cur_path] = {}
            cur_part = cur_part[cur_path]

    return config_copy

def add_item_to_config(config, property_path, value):
    """
    Add an item to a list in config.
    """
    path_components = property_path.split('.')

    # Mutate a copy of the config, not config itself
    cur_part = config_copy = deepcopy(config)
    for i, cur_path in enumerate(path_components):
        if i == len(path_components) - 1:
            # Final component, it must be a list and we append to it
            if cur_path not in cur_part or not _is_list(cur_part[cur_path]):
                cur_part[cur_path] = []
            cur_part = cur_part[cur_path]

            cur_part.append(value)
        else:
            # If we are asked to create new non-leaf nodes, we will always make them dicts
            # This means setting is *destructive* - will replace whatever is down there!
            if cur_path not in cur_part or not _is_dict(cur_part[cur_path]):
                cur_part[cur_path] = {}
            cur_part = cur_part[cur_path]

    return config_copy


def remove_item_from_config(config, property_path, value):
    """
    Add an item to a list in config.
    """
    path_components = property_path.split('.')

    # Mutate a copy of the config, not config itself
    cur_part = config_copy = deepcopy(config)
    for i, cur_path in enumerate(path_components):
        if i == len(path_components) - 1:
            # Final component, it must be a list and we append to it
            if cur_path not in cur_part or not _is_list(cur_part[cur_path]):
                raise ValueError(f'{property_path} is not a list')
            cur_part = cur_part[cur_path]
            cur_part.remove(value)
        else:
            if cur_path not in cur_part or not _is_dict(cur_part[cur_path]):
                raise ValueError(f'{property_path} does not exist in config!')
            cur_part = cur_part[cur_path]

    return config_copy


def show_config(config_path):
    """
    Pretty print config from given config_path
    """
    try:
        with open(config_path) as f:
            config = yaml.load(f)
    except FileNotFoundError:
        config = {}

    yaml.dump(config, sys.stdout)


def set_config_value(config_path, key_path, value):
    """
    Set key at key_path in config_path to value
    """
    # FIXME: Have a file lock here
    # FIXME: Validate schema here
    try:
        with open(config_path) as f:
            config = yaml.load(f)
    except FileNotFoundError:
        config = {}

    config = set_item_in_config(config, key_path, value)

    with open(config_path, 'w') as f:
        yaml.dump(config, f)


def add_config_value(config_path, key_path, value):
    """
    Add value to list at key_path
    """
    # FIXME: Have a file lock here
    # FIXME: Validate schema here
    try:
        with open(config_path) as f:
            config = yaml.load(f)
    except FileNotFoundError:
        config = {}

    config = add_item_to_config(config, key_path, value)

    with open(config_path, 'w') as f:
        yaml.dump(config, f)


def remove_config_value(config_path, key_path, value):
    """
    Remove value from list at key_path
    """
    # FIXME: Have a file lock here
    # FIXME: Validate schema here
    try:
        with open(config_path) as f:
            config = yaml.load(f)
    except FileNotFoundError:
        config = {}

    config = remove_item_from_config(config, key_path, value)

    with open(config_path, 'w') as f:
        yaml.dump(config, f)


def reload_component(component):
    """
    Reload a TLJH component.

    component can be 'hub' or 'proxy'.
    """
    # import here to avoid circular imports
    from tljh import systemd, traefik
    if component == 'hub':
        systemd.restart_service('jupyterhub')
        # FIXME: Verify hub is back up?
        print('Hub reload with new configuration complete')
    elif component == 'proxy':
        traefik.ensure_traefik_config(STATE_DIR)
        systemd.restart_service('configurable-http-proxy')
        systemd.restart_service('traefik')
        print('Proxy reload with new configuration complete')


def parse_value(value_str):
    """Parse a value string"""
    if value_str is None:
        return value_str
    if re.match(r'^\d+$', value_str):
        return int(value_str)
    elif re.match(r'^\d+\.\d*$', value_str):
        return float(value_str)
    elif value_str.lower() == 'true':
        return True
    elif value_str.lower() == 'false':
        return False
    else:
        # it's a string
        return value_str


def _is_dict(item):
    return isinstance(item, Mapping)


def _is_list(item):
    return isinstance(item, Sequence)


def main(argv=None):
    if os.geteuid() != 0:
        print("It looks like this command wasn't run with root privileges. Perhaps you didn't use `sudo -E`?")

    if argv is None:
        argv = sys.argv[1:]

    from .log import init_logging
    try:
        init_logging()
    except Exception as e:
        print(str(e))
        print("Perhaps you didn't use `sudo -E`?")

    argparser = argparse.ArgumentParser()
    argparser.add_argument(
        '--config-path',
        default=CONFIG_FILE,
        help='Path to TLJH config.yaml file'
    )
    subparsers = argparser.add_subparsers(dest='action')

    show_parser = subparsers.add_parser(
        'show',
        help='Show current configuration'
    )

    set_parser = subparsers.add_parser(
        'set',
        help='Set a configuration property'
    )
    set_parser.add_argument(
        'key_path',
        help='Dot separated path to configuration key to set'
    )
    set_parser.add_argument(
        'value',
        help='Value to set the configuration key to'
    )

    add_item_parser = subparsers.add_parser(
        'add-item',
        help='Add a value to a list for a configuration property'
    )
    add_item_parser.add_argument(
        'key_path',
        help='Dot separated path to configuration key to add value to'
    )
    add_item_parser.add_argument(
        'value',
        help='Value to add to the configuration key'
    )

    remove_item_parser = subparsers.add_parser(
        'remove-item',
        help='Remove a value from a list for a configuration property'
    )
    remove_item_parser.add_argument(
        'key_path',
        help='Dot separated path to configuration key to remove value from'
    )
    remove_item_parser.add_argument(
        'value',
        help='Value to remove from key_path'
    )

    reload_parser = subparsers.add_parser(
        'reload',
        help='Reload a component to apply configuration change'
    )
    reload_parser.add_argument(
        'component',
        choices=('hub', 'proxy'),
        help='Which component to reload',
        default='hub',
        nargs='?'
    )

    args = argparser.parse_args(argv)

    if args.action == 'show':
        show_config(args.config_path)
    elif args.action == 'set':
        set_config_value(args.config_path, args.key_path, parse_value(args.value))
    elif args.action == 'add-item':
        add_config_value(args.config_path, args.key_path, parse_value(args.value))
    elif args.action == 'remove-item':
        remove_config_value(args.config_path, args.key_path, parse_value(args.value))
    elif args.action == 'reload':
        reload_component(args.component)
    else:
        argparser.print_help()


if __name__ == '__main__':
    main()
