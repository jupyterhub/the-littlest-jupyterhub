import asyncio
from functools import partial

import pytest
from hubtraf.auth.dummy import login_dummy
from hubtraf.user import User

# Use sudo to invoke it, since this is how users invoke it.
# This catches issues with PATH
TLJH_CONFIG_PATH = ["sudo", "tljh-config"]

# This *must* be localhost, not an IP
# aiohttp throws away cookies if we are connecting to an IP!
HUB_URL = "http://localhost"


# FIXME: Other tests may have set the auth.type to dummy, so we reset it here to
#        get the default of firstuseauthenticator. Tests should cleanup after
#        themselves to a better degree, but its a bit trouble to reload the
#        jupyterhub between each test as well if thats needed...
async def test_restore_relevant_tljh_state():
    assert (
        0
        == await (
            await asyncio.create_subprocess_exec(
                *TLJH_CONFIG_PATH,
                "set",
                "auth.type",
                "firstuseauthenticator.FirstUseAuthenticator",
            )
        ).wait()
    )
    assert (
        0
        == await (
            await asyncio.create_subprocess_exec(*TLJH_CONFIG_PATH, "reload")
        ).wait()
    )


@pytest.mark.parametrize(
    "username, password, expect_successful_login",
    [
        ("test-admin-username", "test-admin-password", True),
        ("user", "", False),
    ],
)
async def test_pre_configured_admin_login(username, password, expect_successful_login):
    """
    Verify that the "--admin <username>:<password>" flag allows that user/pass
    combination and no other user can login.
    """
    async with User(username, HUB_URL, partial(login_dummy, password=password)) as u:
        user_logged_in = await u.login()

    assert user_logged_in == expect_successful_login
