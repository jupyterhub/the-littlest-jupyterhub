"""
Test configurer
"""

from traitlets.config import Config
import os
import sys

from tljh import configurer


def apply_mock_config(overrides):
    """
    Configure a mock configurer with given overrides.

    overrides should be a dict that matches what you parse from a config.yaml
    """
    c = Config()
    configurer.apply_config(overrides, c)
    return c


def test_default_base_url():
    """
    Test default JupyterHub base_url
    """
    c = apply_mock_config({})
    assert c.JupyterHub.base_url == "/"


def test_set_base_url():
    """
    Test set JupyterHub base_url
    """
    c = apply_mock_config({"base_url": "/custom-base"})
    assert c.JupyterHub.base_url == "/custom-base"


def test_default_memory_limit():
    """
    Test default per user memory limit
    """
    c = apply_mock_config({})
    assert c.Spawner.mem_limit is None


def test_set_memory_limit():
    """
    Test setting per user memory limit
    """
    c = apply_mock_config({"limits": {"memory": "42G"}})
    assert c.Spawner.mem_limit == "42G"


def test_app_default():
    """
    Test default application with no config overrides.
    """
    c = apply_mock_config({})
    # default_url is not set, so JupyterHub will pick default.
    assert "default_url" not in c.Spawner


def test_app_jupyterlab():
    """
    Test setting JupyterLab as default application
    """
    c = apply_mock_config({"user_environment": {"default_app": "jupyterlab"}})
    assert c.Spawner.default_url == "/lab"


def test_app_nteract():
    """
    Test setting nteract as default application
    """
    c = apply_mock_config({"user_environment": {"default_app": "nteract"}})
    assert c.Spawner.default_url == "/nteract"


def test_auth_default():
    """
    Test default authentication settings with no overrides
    """
    c = apply_mock_config({})

    assert (
        c.JupyterHub.authenticator_class
        == "firstuseauthenticator.FirstUseAuthenticator"
    )
    # Do not auto create users who haven't been manually added by default
    assert not c.FirstUseAuthenticator.create_users


def test_auth_dummy():
    """
    Test setting Dummy Authenticator & password
    """
    c = apply_mock_config(
        {"auth": {"type": "dummy", "DummyAuthenticator": {"password": "test"}}}
    )
    assert c.JupyterHub.authenticator_class == "dummy"
    assert c.DummyAuthenticator.password == "test"


def test_user_groups():
    """
    Test setting user groups
    """
    c = apply_mock_config(
        {
            "users": {
                "extra_user_groups": {"g1": ["u1", "u2"], "g2": ["u3", "u4"]},
            }
        }
    )
    assert c.UserCreatingSpawner.user_groups == {"g1": ["u1", "u2"], "g2": ["u3", "u4"]}


def test_auth_firstuse():
    """
    Test setting FirstUse Authenticator options
    """
    c = apply_mock_config(
        {
            "auth": {
                "type": "firstuseauthenticator.FirstUseAuthenticator",
                "FirstUseAuthenticator": {"create_users": True},
            }
        }
    )
    assert (
        c.JupyterHub.authenticator_class
        == "firstuseauthenticator.FirstUseAuthenticator"
    )
    assert c.FirstUseAuthenticator.create_users


def test_auth_github():
    """
    Test using GitHub authenticator
    """
    c = apply_mock_config(
        {
            "auth": {
                "type": "oauthenticator.github.GitHubOAuthenticator",
                "GitHubOAuthenticator": {
                    "client_id": "something",
                    "client_secret": "something-else",
                },
            }
        }
    )
    assert (
        c.JupyterHub.authenticator_class == "oauthenticator.github.GitHubOAuthenticator"
    )
    assert c.GitHubOAuthenticator.client_id == "something"
    assert c.GitHubOAuthenticator.client_secret == "something-else"


def test_traefik_api_default():
    """
    Test default traefik api authentication settings with no overrides
    """
    c = apply_mock_config({})

    assert c.TraefikTomlProxy.traefik_api_username == "api_admin"
    assert len(c.TraefikTomlProxy.traefik_api_password) == 0


def test_set_traefik_api():
    """
    Test setting per traefik api credentials
    """
    c = apply_mock_config(
        {"traefik_api": {"username": "some_user", "password": "1234"}}
    )
    assert c.TraefikTomlProxy.traefik_api_username == "some_user"
    assert c.TraefikTomlProxy.traefik_api_password == "1234"


def test_cull_service_default():
    """
    Test default cull service settings with no overrides
    """
    c = apply_mock_config({})

    cull_cmd = [
        sys.executable,
        "-m",
        "jupyterhub_idle_culler",
        "--timeout=600",
        "--cull-every=60",
        "--concurrency=5",
        "--max-age=0",
    ]
    assert c.JupyterHub.services == [
        {
            "name": "cull-idle",
            "admin": True,
            "command": cull_cmd,
        }
    ]


def test_set_cull_service():
    """
    Test setting cull service options
    """
    c = apply_mock_config(
        {"services": {"cull": {"every": 10, "users": True, "max_age": 60}}}
    )
    cull_cmd = [
        sys.executable,
        "-m",
        "jupyterhub_idle_culler",
        "--timeout=600",
        "--cull-every=10",
        "--concurrency=5",
        "--max-age=60",
        "--cull-users",
    ]
    assert c.JupyterHub.services == [
        {
            "name": "cull-idle",
            "admin": True,
            "command": cull_cmd,
        }
    ]


def test_load_secrets(tljh_dir):
    """
    Test loading secret files
    """
    with open(os.path.join(tljh_dir, "state", "traefik-api.secret"), "w") as f:
        f.write("traefik-password")

    tljh_config = configurer.load_config()
    assert tljh_config["traefik_api"]["password"] == "traefik-password"
    c = apply_mock_config(tljh_config)
    assert c.TraefikTomlProxy.traefik_api_password == "traefik-password"


def test_auth_native():
    """
    Test setting Native Authenticator
    """
    c = apply_mock_config(
        {
            "auth": {
                "type": "nativeauthenticator.NativeAuthenticator",
                "NativeAuthenticator": {
                    "open_signup": True,
                },
            }
        }
    )
    assert c.JupyterHub.authenticator_class == "nativeauthenticator.NativeAuthenticator"
    assert c.NativeAuthenticator.open_signup == True
