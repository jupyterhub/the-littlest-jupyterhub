"""
Simplest plugin that exercises all the hooks
"""
from tljh.hooks import hookimpl


@hookimpl
def tljh_extra_user_conda_packages():
    return [
        'hypothesis',
    ]


@hookimpl
def tljh_extra_user_pip_packages():
    return [
        'django',
    ]


@hookimpl
def tljh_extra_apt_packages():
    return [
        'sl',
    ]


@hookimpl
def tljh_config_post_install(config):
    # Put an arbitrary marker we can test for
    config['simplest_plugin'] = {
        'present': True
    }