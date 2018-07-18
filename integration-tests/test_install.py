from contextlib import contextmanager
from concurrent.futures import ProcessPoolExecutor
from functools import partial
import grp
import os
import pwd
import subprocess
import sys
import tempfile

import pytest


ADMIN_GROUP = "jupyterhub-admins"
USER_GROUP = "jupyterhub-users"
INSTALL_PREFIX = os.environ.get("TLJH_INSTALL_PREFIX", "/opt/tljh")


@contextmanager
def noop():
    """no-op context manager

    for parametrized tests
    """
    yield


def setgroup(group):
    """Become the user nobody:group

    Only call in a subprocess because there's no turning back
    """
    gid = grp.getgrnam(group).gr_gid
    uid = pwd.getpwnam("nobody").pw_uid
    os.setgid(gid)
    os.setuid(uid)
    os.environ["HOME"] = "/tmp/test-home-%i-%i" % (uid, gid)


@pytest.mark.parametrize("group", [ADMIN_GROUP, USER_GROUP])
def test_groups_exist(group):
    """Verify that groups exist"""
    grp.getgrnam(group)


def permissions_test(group, path, *, readable=None, writable=None, dirs_only=False):
    """Run a permissions test on all files in a path path"""
    # start a subprocess and become nobody:group in the process
    pool = ProcessPoolExecutor(1)
    pool.submit(setgroup, group)

    def access(path, flag):
        """Run access test in subproccess as nobody:group"""
        return pool.submit(os.access, path, flag).result()

    total_tested = 0

    failures = []

    # walk the directory and check permissions
    for root, dirs, files in os.walk(path):
        to_test = dirs
        if not dirs_only:
            to_test += files
        total_tested += len(to_test)
        for name in to_test:
            path = os.path.join(root, name)
            if os.path.islink(path):
                # skip links
                continue

            # check if the path should be writable
            if writable is not None:
                if access(path, os.W_OK) != writable:
                    failures.append(
                        "{} should {}be writable by {}".format(
                            path, "" if writable else "not ", group
                        )
                    )

            # check if the path should be readable
            if readable is not None:
                if access(path, os.R_OK) != readable:
                    failures.append(
                        "{} should {}be readable by {}".format(
                            path, "" if readable else "not ", group
                        )
                    )
    # verify that we actually tested some files
    # (path typos)
    assert total_tested > 0, "No files to test in %r" % path
    # raise a nice summary of the failures:
    if failures:
        assert False, "\n".join(failures)


def test_admin_writable(group, writable):
    permissions_test(ADMIN_GROUP, sys.prefix, writable=True, dirs_only=True)


@pytest.mark.parametrize("group", [ADMIN_GROUP, USER_GROUP])
def test_all_readable(group):
    # every file in sys.prefix should be readable by everyone
    permissions_test(group, sys.prefix, readable=True)


@pytest.mark.parametrize(
    "group, readwrite", [(ADMIN_GROUP, False), (USER_GROUP, False)]
)
def test_state_permissions(group, readwrite):
    state_dir = os.path.abspath(os.path.join(sys.prefix, os.pardir, "state"))
    permissions_test(group, state_dir, writable=readwrite, readable=readwrite)


@pytest.mark.parametrize("group, allowed", [(USER_GROUP, False), (ADMIN_GROUP, True)])
def test_pip_install(group, allowed):
    if allowed:
        context = noop()
    else:
        context = pytest.raises(subprocess.CalledProcessError)

    with context:
        subprocess.check_call(
            [
                sys.executable,
                "-m",
                "pip",
                "install",
                "--ignore-installed",
                "--no-deps",
                "flit",
            ],
            preexec_fn=partial(setgroup, group),
        )
    if allowed:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "uninstall", "-y", "flit"],
            preexec_fn=partial(setgroup, group),
        )


@pytest.mark.parametrize("group, allowed", [(USER_GROUP, False), (ADMIN_GROUP, True)])
def test_pip_upgrade(group, allowed):
    if allowed:
        context = noop()
    else:
        context = pytest.raises(subprocess.CalledProcessError)
    with context:
        subprocess.check_call(
            [
                sys.executable,
                "-m",
                "pip",
                "install",
                "--ignore-installed",
                "--no-deps",
                "testpath==0.3.0",
            ],
            preexec_fn=partial(setgroup, group),
        )
    if allowed:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "--upgrade", "testpath"],
            preexec_fn=partial(setgroup, group),
        )
