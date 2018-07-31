"""
Commandline interface for setting config items in config.yaml.

Used as:

tljh-config set firstlevel.second_level something

tljh-config show

tljh-config show firstlevel

tljh-config show firstlevel.second_level
"""
import sys
import argparse
from ruamel.yaml import YAML
from copy import deepcopy
from tljh import systemd, traefik


yaml = YAML(typ='rt')


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
            if cur_path not in cur_part or not isinstance(cur_part[cur_path], dict):
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
            if cur_path not in cur_part or not isinstance(cur_part[cur_path], list):
                cur_part[cur_path] = []
            cur_part = cur_part[cur_path]

            cur_part.append(value)
        else:
            # If we are asked to create new non-leaf nodes, we will always make them dicts
            # This means setting is *destructive* - will replace whatever is down there!
            if cur_path not in cur_part or not isinstance(cur_part[cur_path], dict):
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
            if cur_path not in cur_part or not isinstance(cur_part[cur_path], list):
                raise ValueError(f'{property_path} is not a list')
            cur_part = cur_part[cur_path]
            cur_part.remove(value)
        else:
            if cur_path not in cur_part or not isinstance(cur_part[cur_path], dict):
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

def reload_component(component):
    """
    Reload a TLJH component.

    component can be 'hub' or 'proxy'.
    """
    if component == 'hub':
        systemd.restart_service('jupyterhub')
        # FIXME: Verify hub is back up?
        print('Hub reload with new configuration complete')
    elif component == 'proxy':
        # FIXME: How to set path here?
        traefik.ensure_traefik_config('/opt/tljh/hub/state')
        systemd.restart_service('configurable-http-proxy')
        systemd.restart_service('traefik')
        print('Proxy reload with new configuration complete')


def main():
    argparser = argparse.ArgumentParser()
    argparser.add_argument(
        '--config-path',
        default='/opt/tljh/config.yaml',
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
        help='Value ot set the configuration key to'
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

    args = argparser.parse_args()

    if args.action == 'show':
        show_config(args.config_path)
    elif args.action == 'set':
        set_config_value(args.config_path, args.key_path, args.value)
    elif args.action == 'add-item':
        add_config_value(args.config_path, args.key_path, args.value)
    elif args.action == 'remove-item':
        add_config_value(args.config_path, args.key_path, args.value)
    elif args.action == 'reload':
        reload_component(args.component)
    

if __name__ == '__main__':
    main()
