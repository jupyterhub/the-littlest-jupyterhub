import requests
from hubtraf.user import User
from hubtraf.auth.dummy import login_dummy
import secrets
import pytest
from functools import partial
import asyncio
import pwd
import grp
import sys
from tljh.normalize import generate_system_username


# Use sudo to invoke it, since this is how users invoke it.
# This catches issues with PATH
TLJH_CONFIG_PATH = ['sudo', 'tljh-config']

def test_hub_up():
    r = requests.get('http://127.0.0.1')
    r.raise_for_status()


@pytest.mark.asyncio
async def test_user_code_execute():
    """
    User logs in, starts a server & executes code
    """
    # This *must* be localhost, not an IP
    # aiohttp throws away cookies if we are connecting to an IP!
    hub_url = 'http://localhost'
    username = secrets.token_hex(8)

    assert 0 == await (await asyncio.create_subprocess_exec(*TLJH_CONFIG_PATH, 'set', 'auth.type', 'dummyauthenticator.DummyAuthenticator')).wait()
    assert 0 == await (await asyncio.create_subprocess_exec(*TLJH_CONFIG_PATH, 'reload')).wait()

    # FIXME: wait for reload to finish & hub to come up
    # Should be part of tljh-config reload
    await asyncio.sleep(1)

    async with User(username, hub_url, partial(login_dummy, password='')) as u:
            await u.login()
            await u.ensure_server()
            await u.start_kernel()
            await u.assert_code_output("5 * 4", "20", 5, 5)

            # Assert that the user exists
            assert pwd.getpwnam(f'jupyter-{username}') is not None


@pytest.mark.asyncio
async def test_user_admin_add():
    """
    User is made an admin, logs in and we check if they are in admin group
    """
    # This *must* be localhost, not an IP
    # aiohttp throws away cookies if we are connecting to an IP!
    hub_url = 'http://localhost'
    username = secrets.token_hex(8)

    assert 0 == await (await asyncio.create_subprocess_exec(*TLJH_CONFIG_PATH, 'set', 'auth.type', 'dummyauthenticator.DummyAuthenticator')).wait()
    assert 0 == await (await asyncio.create_subprocess_exec(*TLJH_CONFIG_PATH, 'add-item', 'users.admin', username)).wait()
    assert 0 == await (await asyncio.create_subprocess_exec(*TLJH_CONFIG_PATH, 'reload')).wait()

    # FIXME: wait for reload to finish & hub to come up
    # Should be part of tljh-config reload
    await asyncio.sleep(1)
    async with User(username, hub_url, partial(login_dummy, password='')) as u:
            await u.login()
            await u.ensure_server()

            # Assert that the user exists
            assert pwd.getpwnam(f'jupyter-{username}') is not None

            # Assert that the user has admin rights
            assert f'jupyter-{username}' in grp.getgrnam('jupyterhub-admins').gr_mem


@pytest.mark.asyncio
async def test_user_admin_remove():
    """
    User is made an admin, logs in and we check if they are in admin group.

    Then we remove them from admin group, and check they *aren't* in admin group :D
    """
    # This *must* be localhost, not an IP
    # aiohttp throws away cookies if we are connecting to an IP!
    hub_url = 'http://localhost'
    username = secrets.token_hex(8)

    assert 0 == await (await asyncio.create_subprocess_exec(*TLJH_CONFIG_PATH, 'set', 'auth.type', 'dummyauthenticator.DummyAuthenticator')).wait()
    assert 0 == await (await asyncio.create_subprocess_exec(*TLJH_CONFIG_PATH, 'add-item', 'users.admin', username)).wait()
    assert 0 == await (await asyncio.create_subprocess_exec(*TLJH_CONFIG_PATH, 'reload')).wait()

    # FIXME: wait for reload to finish & hub to come up
    # Should be part of tljh-config reload
    await asyncio.sleep(1)
    async with User(username, hub_url, partial(login_dummy, password='')) as u:
            await u.login()
            await u.ensure_server()

            # Assert that the user exists
            assert pwd.getpwnam(f'jupyter-{username}') is not None

            # Assert that the user has admin rights
            assert f'jupyter-{username}' in grp.getgrnam('jupyterhub-admins').gr_mem


            assert 0 == await (await asyncio.create_subprocess_exec(*TLJH_CONFIG_PATH, 'remove-item', 'users.admin', username)).wait()
            assert 0 == await (await asyncio.create_subprocess_exec(*TLJH_CONFIG_PATH, 'reload')).wait()
            await asyncio.sleep(1)

            await u.stop_server()
            await u.ensure_server()

            # Assert that the user does *not* have admin rights
            assert f'jupyter-{username}' in grp.getgrnam('jupyterhub-admins').gr_mem


@pytest.mark.asyncio
async def test_long_username():
    """
    User with a long name logs in, and we check if their name is properly truncated.
    """
    # This *must* be localhost, not an IP
    # aiohttp throws away cookies if we are connecting to an IP!
    hub_url = 'http://localhost'
    username = secrets.token_hex(32)

    assert 0 == await (await asyncio.create_subprocess_exec(*TLJH_CONFIG_PATH, 'set', 'auth.type', 'dummyauthenticator.DummyAuthenticator')).wait()
    assert 0 == await (await asyncio.create_subprocess_exec(*TLJH_CONFIG_PATH, 'reload')).wait()

    # FIXME: wait for reload to finish & hub to come up
    # Should be part of tljh-config reload
    await asyncio.sleep(1)
    try:
        async with User(username, hub_url, partial(login_dummy, password='')) as u:
                await u.login()
                await u.ensure_server()

                # Assert that the user exists
                system_username = generate_system_username(f'jupyter-{username}')
                assert pwd.getpwnam(system_username) is not None

                await u.stop_server()
    except:
        # If we have any errors, print jupyterhub logs before exiting
        subprocess.check_call([
            'journalctl',
            '-u', 'jupyterhub',
            '--no-pager'
        ])
        raise