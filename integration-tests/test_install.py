from contextlib import contextmanager
from concurrent.futures import ProcessPoolExecutor
from functools import partial
import grp
import os
import pwd
import subprocess
import sys

import pytest


ADMIN_GROUP = "jupyterhub-admins"
USER_GROUP = "jupyterhub-users"
INSTALL_PREFIX = os.environ.get("TLJH_INSTALL_PREFIX", "/opt/tljh")
HUB_PREFIX = os.path.join(INSTALL_PREFIX, "hub")
USER_PREFIX = os.path.join(INSTALL_PREFIX, "user")
STATE_DIR = os.path.join(INSTALL_PREFIX, "state")


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
            st = os.lstat(path)
            try:
                user = pwd.getpwuid(st.st_uid).pw_name
            except KeyError:
                # uid may not exist
                user = st.st_uid
            try:
                groupname = grp.getgrgid(st.st_gid).gr_name
            except KeyError:
                # gid may not exist
                groupname = st.st_gid
            stat_str = "{perm:04o} {user} {group}".format(
                perm=st.st_mode, user=user, group=groupname
            )

            # check if the path should be writable
            if writable is not None:
                if access(path, os.W_OK) != writable:
                    failures.append(
                        "{} {} should {}be writable by {}".format(
                            stat_str, path, "" if writable else "not ", group
                        )
                    )

            # check if the path should be readable
            if readable is not None:
                if access(path, os.R_OK) != readable:
                    failures.append(
                        "{} {} should {}be readable by {}".format(
                            stat_str, path, "" if readable else "not ", group
                        )
                    )
    # verify that we actually tested some files
    # (path typos)
    assert total_tested > 0, "No files to test in %r" % path
    # raise a nice summary of the failures:
    if failures:
        if len(failures) > 50:
            failures = failures[:32] + ["...%i total" % len(failures)]
        assert False, "\n".join(failures)


@pytest.mark.xfail(reason="admin-write permissions is not implemented")
def test_admin_writable():
    permissions_test(ADMIN_GROUP, sys.prefix, writable=True, dirs_only=True)


def test_installer_log_readable():
    # Test that installer.log is owned by root, and not readable by anyone else
    file_stat = os.stat("/opt/tljh/installer.log")
    assert file_stat.st_uid == 0
    assert file_stat.st_mode == 0o100500


@pytest.mark.parametrize("group", [ADMIN_GROUP, USER_GROUP])
def test_user_env_readable(group):
    # every file in user env should be readable by everyone
    permissions_test(group, USER_PREFIX, readable=True)


def test_nothing_user_writable():
    # nothing in the install directory should be writable by users
    permissions_test(USER_GROUP, INSTALL_PREFIX, writable=False)


@pytest.mark.parametrize(
    "group, readwrite", [(ADMIN_GROUP, False), (USER_GROUP, False)]
)
def test_state_permissions(group, readwrite):
    state_dir = os.path.abspath(os.path.join(sys.prefix, os.pardir, "state"))
    permissions_test(group, state_dir, writable=readwrite, readable=readwrite)


# FIXME: admin-group should have install permissions
@pytest.mark.parametrize(
    "group, allowed",
    [
        (USER_GROUP, False),
        pytest.param(
            ADMIN_GROUP,
            True,
            marks=pytest.mark.xfail(reason="admin-permissions not implemented"),
        ),
    ],
)
def test_pip_install(group, allowed):
    if allowed:
        context = noop()
    else:
        context = pytest.raises(subprocess.CalledProcessError)

    python = os.path.join(USER_PREFIX, "bin", "python")

    with context:
        # we explicitly add `--no-user` here even though a real user wouldn't
        # With this test we want to check that a user can't install to the
        # global site-packages directory. In new versions of pip the default
        # behaviour is to install to a user location when a global install
        # isn't possible. By using --no-user we disable this behaviour and
        # get a failure if the user can't install to the global site. Which is
        # what we wanted to test for here.
        subprocess.check_call(
            [
                python,
                "-m",
                "pip",
                "install",
                "--no-user",
                "--ignore-installed",
                "--no-deps",
                "flit",
            ],
            preexec_fn=partial(setgroup, group),
        )
    if allowed:
        subprocess.check_call(
            [python, "-m", "pip", "uninstall", "-y", "flit"],
            preexec_fn=partial(setgroup, group),
        )


@pytest.mark.parametrize(
    "group, allowed",
    [
        (USER_GROUP, False),
        pytest.param(
            ADMIN_GROUP,
            True,
            marks=pytest.mark.xfail(reason="admin-permissions not implemented"),
        ),
    ],
)
def test_pip_upgrade(group, allowed):
    if allowed:
        context = noop()
        pytest.skip("admin-install permissions is not implemented")
    else:
        context = pytest.raises(subprocess.CalledProcessError)
    python = os.path.join(USER_PREFIX, "bin", "python")
    with context:
        subprocess.check_call(
            [
                python,
                "-m",
                "pip",
                "install",
                "--no-user",
                "--ignore-installed",
                "--no-deps",
                "testpath==0.3.0",
            ],
            preexec_fn=partial(setgroup, group),
        )
    if allowed:
        subprocess.check_call(
            [python, "-m", "pip", "install", "--upgrade", "testpath"],
            preexec_fn=partial(setgroup, group),
        )


def test_symlinks():
    """
    Test we symlink tljh-config to /usr/local/bin
    """
    assert os.path.exists("/usr/bin/tljh-config")
