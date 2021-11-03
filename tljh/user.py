"""
User management for tljh.

Supports minimal user & group management
"""
import grp
import pwd
import subprocess
from os.path import expanduser

# Set up plugin infrastructure
from tljh.utils import get_plugin_manager


def ensure_user(username):
    """
    Make sure a given user exists
    """
    # Check if user exists
    try:
        pwd.getpwnam(username)
        # User exists, nothing to do!
        return
    except KeyError:
        # User doesn't exist, time to create!
        pass

    subprocess.check_call(["useradd", "--create-home", username])

    subprocess.check_call(["chmod", "o-rwx", expanduser(f"~{username}")])

    pm = get_plugin_manager()
    pm.hook.tljh_new_user_create(username=username)


def remove_user(username):
    """
    Remove user from system if exists
    """
    try:
        pwd.getpwnam(username)
    except KeyError:
        # User doesn't exist, nothing to do
        return

    subprocess.check_call(["deluser", "--quiet", username])


def ensure_group(groupname):
    """
    Ensure given group exists
    """
    subprocess.check_call(["groupadd", "--force", groupname])


def remove_group(groupname):
    """
    Remove group from system if exists
    """
    try:
        grp.getgrnam(groupname)
    except KeyError:
        # Group doesn't exist, nothing to do
        return

    subprocess.check_call(["delgroup", "--quiet", groupname])


def ensure_user_group(username, groupname):
    """
    Ensure given user is member of given group

    Group and User must already exist.
    """
    group = grp.getgrnam(groupname)
    if username in group.gr_mem:
        return

    subprocess.check_call(["gpasswd", "--add", username, groupname])


def remove_user_group(username, groupname):
    """
    Ensure given user is *not* a member of given group
    """
    group = grp.getgrnam(groupname)
    if username not in group.gr_mem:
        return

    subprocess.check_call(["gpasswd", "--delete", username, groupname])
