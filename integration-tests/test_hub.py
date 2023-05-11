import requests
from hubtraf.user import User
from hubtraf.auth.dummy import login_dummy
from jupyterhub.utils import exponential_backoff
import secrets
import pytest
from functools import partial
import asyncio
import pwd
import grp
import subprocess
from os import system
from tljh.normalize import generate_system_username
from packaging.version import Version as V

# Use sudo to invoke it, since this is how users invoke it.
# This catches issues with PATH
TLJH_CONFIG_PATH = ["sudo", "tljh-config"]

# This *must* be localhost, not an IP
# aiohttp throws away cookies if we are connecting to an IP!
hub_url = "http://localhost"


def test_hub_up():
    r = requests.get(hub_url)
    r.raise_for_status()


def test_hub_version():
    r = requests.get(hub_url + "/hub/api")
    r.raise_for_status()
    info = r.json()
    assert V("3.0") <= V(info["version"]) <= V("4.0")


@pytest.mark.asyncio
async def test_user_code_execute():
    """
    User logs in, starts a server & executes code
    """
    username = secrets.token_hex(8)

    assert (
        0
        == await (
            await asyncio.create_subprocess_exec(
                *TLJH_CONFIG_PATH, "set", "auth.type", "dummy"
            )
        ).wait()
    )
    assert (
        0
        == await (
            await asyncio.create_subprocess_exec(*TLJH_CONFIG_PATH, "reload")
        ).wait()
    )

    async with User(username, hub_url, partial(login_dummy, password="")) as u:
        await u.login()
        await u.ensure_server_simulate()
        await u.start_kernel()
        await u.assert_code_output("5 * 4", "20", 5, 5)

        # Assert that the user exists
        assert pwd.getpwnam(f"jupyter-{username}") is not None


@pytest.mark.asyncio
async def test_user_server_started_with_custom_base_url():
    """
    User logs in, starts a server with a custom base_url & executes code
    """
    # This *must* be localhost, not an IP
    # aiohttp throws away cookies if we are connecting to an IP!
    base_url = "/custom-base"
    hub_url = f"http://localhost{base_url}"
    username = secrets.token_hex(8)

    assert (
        0
        == await (
            await asyncio.create_subprocess_exec(
                *TLJH_CONFIG_PATH, "set", "auth.type", "dummy"
            )
        ).wait()
    )
    assert (
        0
        == await (
            await asyncio.create_subprocess_exec(
                *TLJH_CONFIG_PATH, "set", "base_url", base_url
            )
        ).wait()
    )
    assert (
        0
        == await (
            await asyncio.create_subprocess_exec(*TLJH_CONFIG_PATH, "reload")
        ).wait()
    )

    async with User(username, hub_url, partial(login_dummy, password="")) as u:
        await u.login()
        await u.ensure_server_simulate()

        # unset base_url to avoid problems with other tests
        assert (
            0
            == await (
                await asyncio.create_subprocess_exec(
                    *TLJH_CONFIG_PATH, "unset", "base_url"
                )
            ).wait()
        )
        assert (
            0
            == await (
                await asyncio.create_subprocess_exec(*TLJH_CONFIG_PATH, "reload")
            ).wait()
        )


@pytest.mark.asyncio
async def test_user_admin_add():
    """
    User is made an admin, logs in and we check if they are in admin group
    """
    # This *must* be localhost, not an IP
    # aiohttp throws away cookies if we are connecting to an IP!
    hub_url = "http://localhost"
    username = secrets.token_hex(8)

    assert (
        0
        == await (
            await asyncio.create_subprocess_exec(
                *TLJH_CONFIG_PATH, "set", "auth.type", "dummy"
            )
        ).wait()
    )
    assert (
        0
        == await (
            await asyncio.create_subprocess_exec(
                *TLJH_CONFIG_PATH, "add-item", "users.admin", username
            )
        ).wait()
    )
    assert (
        0
        == await (
            await asyncio.create_subprocess_exec(*TLJH_CONFIG_PATH, "reload")
        ).wait()
    )

    async with User(username, hub_url, partial(login_dummy, password="")) as u:
        await u.login()
        await u.ensure_server_simulate()

        # Assert that the user exists
        assert pwd.getpwnam(f"jupyter-{username}") is not None

        # Assert that the user has admin rights
        assert f"jupyter-{username}" in grp.getgrnam("jupyterhub-admins").gr_mem


# FIXME: Make this test pass
@pytest.mark.asyncio
@pytest.mark.xfail(reason="Unclear why this is failing")
async def test_user_admin_remove():
    """
    User is made an admin, logs in and we check if they are in admin group.

    Then we remove them from admin group, and check they *aren't* in admin group :D
    """
    # This *must* be localhost, not an IP
    # aiohttp throws away cookies if we are connecting to an IP!
    hub_url = "http://localhost"
    username = secrets.token_hex(8)

    assert (
        0
        == await (
            await asyncio.create_subprocess_exec(
                *TLJH_CONFIG_PATH, "set", "auth.type", "dummy"
            )
        ).wait()
    )
    assert (
        0
        == await (
            await asyncio.create_subprocess_exec(
                *TLJH_CONFIG_PATH, "add-item", "users.admin", username
            )
        ).wait()
    )
    assert (
        0
        == await (
            await asyncio.create_subprocess_exec(*TLJH_CONFIG_PATH, "reload")
        ).wait()
    )

    async with User(username, hub_url, partial(login_dummy, password="")) as u:
        await u.login()
        await u.ensure_server_simulate()

        # Assert that the user exists
        assert pwd.getpwnam(f"jupyter-{username}") is not None

        # Assert that the user has admin rights
        assert f"jupyter-{username}" in grp.getgrnam("jupyterhub-admins").gr_mem

        assert (
            0
            == await (
                await asyncio.create_subprocess_exec(
                    *TLJH_CONFIG_PATH, "remove-item", "users.admin", username
                )
            ).wait()
        )
        assert (
            0
            == await (
                await asyncio.create_subprocess_exec(*TLJH_CONFIG_PATH, "reload")
            ).wait()
        )

        await u.stop_server()
        await u.ensure_server_simulate()

        # Assert that the user does *not* have admin rights
        assert f"jupyter-{username}" not in grp.getgrnam("jupyterhub-admins").gr_mem


@pytest.mark.asyncio
async def test_long_username():
    """
    User with a long name logs in, and we check if their name is properly truncated.
    """
    # This *must* be localhost, not an IP
    # aiohttp throws away cookies if we are connecting to an IP!
    hub_url = "http://localhost"
    username = secrets.token_hex(32)

    assert (
        0
        == await (
            await asyncio.create_subprocess_exec(
                *TLJH_CONFIG_PATH, "set", "auth.type", "dummy"
            )
        ).wait()
    )
    assert (
        0
        == await (
            await asyncio.create_subprocess_exec(*TLJH_CONFIG_PATH, "reload")
        ).wait()
    )

    try:
        async with User(username, hub_url, partial(login_dummy, password="")) as u:
            await u.login()
            await u.ensure_server_simulate()

            # Assert that the user exists
            system_username = generate_system_username(f"jupyter-{username}")
            assert pwd.getpwnam(system_username) is not None

            await u.stop_server()
    except:
        # If we have any errors, print jupyterhub logs before exiting
        subprocess.check_call(["journalctl", "-u", "jupyterhub", "--no-pager"])
        raise


@pytest.mark.asyncio
async def test_user_group_adding():
    """
    User logs in, and we check if they are added to the specified group.
    """
    # This *must* be localhost, not an IP
    # aiohttp throws away cookies if we are connecting to an IP!
    hub_url = "http://localhost"
    username = secrets.token_hex(8)
    groups = {"somegroup": [username]}
    # Create the group we want to add the user to
    system("groupadd somegroup")

    assert (
        0
        == await (
            await asyncio.create_subprocess_exec(
                *TLJH_CONFIG_PATH, "set", "auth.type", "dummy"
            )
        ).wait()
    )
    assert (
        0
        == await (
            await asyncio.create_subprocess_exec(
                *TLJH_CONFIG_PATH,
                "add-item",
                "users.extra_user_groups.somegroup",
                username,
            )
        ).wait()
    )
    assert (
        0
        == await (
            await asyncio.create_subprocess_exec(*TLJH_CONFIG_PATH, "reload")
        ).wait()
    )

    try:
        async with User(username, hub_url, partial(login_dummy, password="")) as u:
            await u.login()
            await u.ensure_server_simulate()

            # Assert that the user exists
            system_username = generate_system_username(f"jupyter-{username}")
            assert pwd.getpwnam(system_username) is not None

            # Assert that the user was added to the specified group
            assert f"jupyter-{username}" in grp.getgrnam("somegroup").gr_mem

            await u.stop_server()
            # Delete the group
            system("groupdel somegroup")
    except:
        # If we have any errors, print jupyterhub logs before exiting
        subprocess.check_call(["journalctl", "-u", "jupyterhub", "--no-pager"])
        raise


@pytest.mark.asyncio
async def test_idle_server_culled():
    """
    User logs in, starts a server & stays idle for 1 min.
    (the user's server should be culled during this period)
    """
    # This *must* be localhost, not an IP
    # aiohttp throws away cookies if we are connecting to an IP!
    hub_url = "http://localhost"
    username = secrets.token_hex(8)

    assert (
        0
        == await (
            await asyncio.create_subprocess_exec(
                *TLJH_CONFIG_PATH, "set", "auth.type", "dummy"
            )
        ).wait()
    )
    # Check every 5s for idle servers to cull
    assert (
        0
        == await (
            await asyncio.create_subprocess_exec(
                *TLJH_CONFIG_PATH, "set", "services.cull.every", "5"
            )
        ).wait()
    )
    # Apart from servers, also cull users
    assert (
        0
        == await (
            await asyncio.create_subprocess_exec(
                *TLJH_CONFIG_PATH, "set", "services.cull.users", "True"
            )
        ).wait()
    )
    # Cull servers and users after 30s, regardless of activity
    assert (
        0
        == await (
            await asyncio.create_subprocess_exec(
                *TLJH_CONFIG_PATH, "set", "services.cull.max_age", "30"
            )
        ).wait()
    )
    assert (
        0
        == await (
            await asyncio.create_subprocess_exec(*TLJH_CONFIG_PATH, "reload")
        ).wait()
    )

    async with User(username, hub_url, partial(login_dummy, password="")) as u:
        await u.login()
        # Start user's server
        await u.ensure_server_simulate()
        # Assert that the user exists
        assert pwd.getpwnam(f"jupyter-{username}") is not None

        # Check that we can get to the user's server
        user_url = u.notebook_url / "api/status"
        r = await u.session.get(user_url, allow_redirects=False)
        assert r.status == 200

        # Check that we can talk to JupyterHub itself
        # use this as a proxy for whether the user still exists
        async def hub_api_request():
            r = await u.session.get(
                u.hub_url / "hub/api/user",
                headers={"Referer": str(u.hub_url / "hub/")},
                allow_redirects=False,
            )
            return r

        r = await hub_api_request()
        assert r.status == 200

        # Wait for culling
        # step 1: check if the server is still running
        timeout = 100

        async def server_stopped():
            """Has the server been stopped?"""
            r = await u.session.get(user_url, allow_redirects=False)
            print(f"{r.status} {r.url}")
            return r.status != 200

        await exponential_backoff(
            server_stopped,
            "Server still running!",
            timeout=timeout,
        )

        # step 2. wait for user to be deleted
        async def user_removed():
            # Check that after 60s, the user has been culled
            r = await hub_api_request()
            print(f"{r.status} {r.url}")
            return r.status == 403

        await exponential_backoff(
            user_removed,
            "User still exists!",
            timeout=timeout,
        )


@pytest.mark.asyncio
async def test_active_server_not_culled():
    """
    User logs in, starts a server & stays idle for 30s
    (the user's server should not be culled during this period).
    """
    # This *must* be localhost, not an IP
    # aiohttp throws away cookies if we are connecting to an IP!
    hub_url = "http://localhost"
    username = secrets.token_hex(8)

    assert (
        0
        == await (
            await asyncio.create_subprocess_exec(
                *TLJH_CONFIG_PATH, "set", "auth.type", "dummy"
            )
        ).wait()
    )
    # Check every 5s for idle servers to cull
    assert (
        0
        == await (
            await asyncio.create_subprocess_exec(
                *TLJH_CONFIG_PATH, "set", "services.cull.every", "5"
            )
        ).wait()
    )
    # Apart from servers, also cull users
    assert (
        0
        == await (
            await asyncio.create_subprocess_exec(
                *TLJH_CONFIG_PATH, "set", "services.cull.users", "True"
            )
        ).wait()
    )
    # Cull servers and users after 30s, regardless of activity
    assert (
        0
        == await (
            await asyncio.create_subprocess_exec(
                *TLJH_CONFIG_PATH, "set", "services.cull.max_age", "60"
            )
        ).wait()
    )
    assert (
        0
        == await (
            await asyncio.create_subprocess_exec(*TLJH_CONFIG_PATH, "reload")
        ).wait()
    )

    async with User(username, hub_url, partial(login_dummy, password="")) as u:
        await u.login()
        # Start user's server
        await u.ensure_server_simulate()
        # Assert that the user exists
        assert pwd.getpwnam(f"jupyter-{username}") is not None

        # Check that we can get to the user's server
        user_url = u.notebook_url / "api/status"
        r = await u.session.get(user_url, allow_redirects=False)
        assert r.status == 200

        async def server_has_stopped():
            # Check that after 30s, we can still reach the user's server
            r = await u.session.get(user_url, allow_redirects=False)
            print(f"{r.status} {r.url}")
            return r.status != 200

        try:
            await exponential_backoff(
                server_has_stopped,
                "User's server is still reachable (good!)",
                timeout=30,
            )
        except asyncio.TimeoutError:
            # timeout error means the test passed - the server didn't go away while we were waiting
            pass
        else:
            pytest.fail(f"Server at {user_url} got culled prematurely!")
