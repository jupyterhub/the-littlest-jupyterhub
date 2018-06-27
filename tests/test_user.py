"""
Test wrappers in tljw.user module
"""
from tljh import user
import os
import uuid
import pwd
import grp
import pytest


def test_ensure_user():
    """
    Test user creation & removal
    """
    # Use a prefix to make sure we never start with a number
    username = 'u' + str(uuid.uuid4())[:8]
    # Validate that no user exists
    with pytest.raises(KeyError):
        pwd.getpwnam(username)

    try:
        # Create user!
        user.ensure_user(username)
        # This raises exception if user doesn't exist
        ent = pwd.getpwnam(username)
        # Home directory must also exist
        assert os.path.exists(ent.pw_shell)
        # Run ensure_user again, should be a noop
        user.ensure_user(username)
        # User still exists, after our second ensure_user call
        pwd.getpwnam(username)
    finally:
        # We clean up and remove user!
        user.remove_user(username)
        with pytest.raises(KeyError):
            pwd.getpwnam(username)


def test_ensure_group():
    """
    Test group creation & removal
    """
    # Use a prefix to make sure we never start with a number
    groupname = 'g' + str(uuid.uuid4())[:8]

    # Validate that no group exists
    with pytest.raises(KeyError):
        grp.getgrnam(groupname)

    try:
        # Create group
        user.ensure_group(groupname)
        # This raises if group doesn't exist
        grp.getgrnam(groupname)

        # Do it again, this should be a noop
        user.ensure_group(groupname)
        grp.getgrnam(groupname)
    finally:
        # Remove the group
        user.remove_group(groupname)
        with pytest.raises(KeyError):
            grp.getgrnam(groupname)


def test_group_membership():
    """
    Test group memberships can be added / removed
    """
    username = 'u' + str(uuid.uuid4())[:8]
    groupname = 'g' + str(uuid.uuid4())[:8]

    # Validate that no group exists
    with pytest.raises(KeyError):
        grp.getgrnam(groupname)
    with pytest.raises(KeyError):
        pwd.getpwnam(username)

    try:
        user.ensure_group(groupname)
        user.ensure_user(username)

        user.ensure_user_group(username, groupname)

        assert username in grp.getgrnam(groupname).gr_mem

        # Do it again, this should be a noop
        user.ensure_user_group(username, groupname)

        assert username in grp.getgrnam(groupname).gr_mem

        # Remove it
        user.remove_user_group(username, groupname)
        assert username not in grp.getgrnam(groupname).gr_mem

        # Do it again, this should be a noop
        user.remove_user_group(username, groupname)
        assert username not in grp.getgrnam(groupname).gr_mem
    finally:
        # Remove the group
        user.remove_user(username)
        user.remove_group(groupname)

        with pytest.raises(KeyError):
            grp.getgrnam(groupname)
        with pytest.raises(KeyError):
            pwd.getpwnam(username)
