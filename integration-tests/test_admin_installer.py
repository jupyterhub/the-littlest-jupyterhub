from functools import partial

import pytest
from hubtraf.auth.dummy import login_dummy
from hubtraf.user import User

hub_url = "http://localhost"


async def test_admin_login():
    """
    Test if the admin that was added during install can login with
    the password provided.
    """
    username = "test-admin-username"
    password = "test-admin-password"

    async with User(username, hub_url, partial(login_dummy, password=password)) as u:
        await u.login()
        # If user is not logged in, this will raise an exception
        await u.ensure_server_simulate(timeout=60, spawn_refresh_time=5)


@pytest.mark.parametrize(
    "username, password",
    [
        ("test-admin-username", ""),
        ("test-admin-username", "wrong_passw"),
        ("user", "password"),
    ],
)
async def test_unsuccessful_login(username, password):
    """
    Ensure nobody but the admin that was added during install can login
    """
    async with User(username, hub_url, partial(login_dummy, password="")) as u:
        user_logged_in = await u.login()

    assert user_logged_in == False
