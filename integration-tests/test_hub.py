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

    async with User(username, hub_url, partial(login_dummy, password='')) as u:
            await u.login()
            await u.ensure_server()
            await u.start_kernel()
            await u.assert_code_output("5 * 4", "20", 5, 5)

            # Assert that the user exists
            assert pwd.getpwnam(f'jupyter-{username}') is not None


@pytest.mark.asyncio
async def test_user_admin_code():
    """
    User logs in, starts a server & executes code
    """
    # This *must* be localhost, not an IP
    # aiohttp throws away cookies if we are connecting to an IP!
    hub_url = 'http://localhost'
    username = secrets.token_hex(8)

    tljh_config_path = [sys.executable, '-m', 'tljh.config']

    assert 0 == await (await asyncio.create_subprocess_exec(*tljh_config_path, 'add-item', 'users.admin', username)).wait()
    assert 0 == await (await asyncio.create_subprocess_exec(*tljh_config_path, 'reload')).wait()

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

            # Assert that the user has admin rights
            assert f'jupyter-{username}' in grp.getgrnam('jupyterhub-admins').gr_mem