"""
User management for tljh.

Supports minimal user & group management
"""
import os
import pwd
import grp
import stat
import subprocess


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

    subprocess.check_call([
        'useradd',
        '--create-home',
        username
    ])


def remove_user(username):
    """
    Remove user from system if exists
    """
    try:
        pwd.getpwnam(username)
    except KeyError:
        # User doesn't exist, nothing to do
        return

    subprocess.check_call([
        'deluser',
        '--quiet',
        username
    ])


def ensure_group(groupname):
    """
    Ensure given group exists
    """
    subprocess.check_call([
        'groupadd',
        '--force',
        groupname
    ])


def remove_group(groupname):
    """
    Remove group from system if exists
    """
    try:
        grp.getgrnam(groupname)
    except KeyError:
        # Group doesn't exist, nothing to do
        return

    subprocess.check_call([
        'delgroup',
        '--quiet',
        groupname
    ])


def ensure_user_group(username, groupname):
    """
    Ensure given user is member of given group

    Group and User must already exist.
    """
    group = grp.getgrnam(groupname)
    if username in group.gr_mem:
        return

    subprocess.check_call([
        'gpasswd',
        '--add',
        username,
        groupname
    ])


def remove_user_group(username, groupname):
    """
    Ensure given user is *not* a member of given group
    """
    group = grp.getgrnam(groupname)
    if username not in group.gr_mem:
        return

    subprocess.check_call([
        'gpasswd',
        '--delete',
        username,
        groupname
    ])


def _ensure_group_owner(gid, path, *, isdir):
    """Ensure a file or directory is owned by a group"""

    # check and update owner group
    st = os.lstat(path)
    if st.st_gid != gid:
        # ensure owned by gid
        os.chown(path, st.st_uid, gid, follow_symlinks=False)

    # check and update permissions
    if os.chmod not in os.supports_follow_symlinks:
        follow_symlinks = True
        if os.path.islink(path):
            # can't chmod symlinks on e.g. linux
            return
    else:
        follow_symlinks = False

    correct_mode = current_mode = os.lstat(path).st_mode
    if isdir:
        # setgid bit on directories so new files have the right group
        # all directories should have srwX permissions
        correct_mode |= stat.S_ISGID | stat.S_IRWXG
    else:
        # group read-write
        correct_mode |= stat.S_IRGRP | stat.S_IWGRP
        # add group-executable if user-executable
        if current_mode & stat.S_IXUSR:
            correct_mode |= stat.S_IXGRP

    # if mode is not correct, change it
    if correct_mode != current_mode:
        os.chmod(path, correct_mode, follow_symlinks=follow_symlinks)


def ensure_group_permissions(groupname, path):
    """Ensure a directory has permissions to be administered by a group

    - all files are owned by groupname
    - setgid bit so new files are owned by groupname by default
    - setfacl so new files are group-writable by default
    """

    gid = grp.getgrnam(groupname).gr_gid
    _ensure_group_owner(gid, path, isdir=True)
    # setfacl on the root so new files are group-writable
    subprocess.check_call(["setfacl", "-d", "-m", "g::rwX", path])
    # recursively check permissions to make sure it's in the initial right state
    for root, dirs, files in os.walk(path):
        for d in dirs:
            d = os.path.join(root, d)
            _ensure_group_owner(gid, d, isdir=True)
        for f in files:
            f = os.path.join(root, f)
            _ensure_group_owner(gid, f, isdir=False)
