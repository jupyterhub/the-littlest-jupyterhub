from hubtraf.user import User
from hubtraf.auth.dummy import login_dummy
import pytest
from functools import partial


@pytest.mark.asyncio
async def test_admin_login():
    """
    Test if the admin that was added during install can login with
    the password provided.
    """
    hub_url = "http://localhost"
    username = "admin"
    password = "admin"

    async with User(username, hub_url, partial(login_dummy, password=password)) as u:
        await u.login()
        # If user is not logged in, this will raise an exception
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
    hub_url = "http://localhost"

    async with User(username, hub_url, partial(login_dummy, password="")) as u:
        user_logged_in = await u.login()

    assert user_logged_in == False
