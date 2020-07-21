from hubtraf.user import User
from hubtraf.auth.dummy import login_dummy
import pytest
from functools import partial
import asyncio


@pytest.mark.asyncio
async def test_admin_login():
    """
    Test if the admin that was added during install can login with
    the password provided.
    """
    hub_url = 'http://localhost'
    username = "admin"
    password = "admin"

    async with User(username, hub_url, partial(login_dummy, password=password)) as u:
            await u.login()
            await u.ensure_server_simulate()


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "username, password",
    [
        ("admin", ""),
        ("admin", "wrong_passw"),
        ("user", "password"),
    ],
)
async def test_unsuccessful_login(username, password):
    """
    Ensure nobody but the admin that was added during install can login
    """
    hub_url = 'http://localhost'

    try:
        async with User(username, hub_url, partial(login_dummy, password="")) as u:
                await u.login()
    except Exception:
        # This is what we except to happen
        pass
    else:
        raise
