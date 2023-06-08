from functools import partial

import pytest
from hubtraf.auth.dummy import login_dummy
from hubtraf.user import User

hub_url = "http://localhost"


@pytest.mark.parametrize(
    "username, password, expect_successful_login",
    [
        ("test-admin-username", "wrong_passw", False),
        ("test-admin-username", "test-admin-password", True),
        ("test-admin-username", "", False),
        ("user", "", False),
        ("user", "password", False),
    ],
)
async def test_pre_configured_admin_login(username, password, expect_successful_login):
    """
    Verify that the "--admin <username>:<password>" flag allows that user/pass
    combination and no other user can login.
    """
    async with User(username, hub_url, partial(login_dummy, password=password)) as u:
        user_logged_in = await u.login()

    assert user_logged_in == expect_successful_login
