"""
Unit test functions to test JSON Schema validation
"""

import pytest

from tljh import config


@pytest.mark.parametrize(
    "valid_config",
    [
        # Valid configuration with JupyterLab as default app and HTTPS enabled with Let's Encrypt
        {
            "user_environment": {"default_app": "jupyterlab"},
            "https": {
                "enabled": True,
                "letsencrypt": {
                    "email": "admin@example.com",
                    "domains": ["example.com"],
                },
            },
        },
        # Valid configuration with classic notebook UI
        {"user_environment": {"default_app": "classic"}, "https": {"enabled": False}},
        # Valid configuration with culling service enabled
        {
            "user_environment": {"default_app": "jupyterlab"},
            "https": {"enabled": False},
            "services": {
                "cull": {
                    "enabled": True,
                    "timeout": 3600,
                    "every": 600,
                    "concurrency": 5,
                    "users": True,
                    "max_age": 86400,
                    "remove_named_servers": False,
                }
            },
        },
        # Valid configuration of resource limits
        {
            "user_environment": {"default_app": "jupyterlab"},
            "https": {"enabled": False},
            "limits": {"memory": "2G", "cpu": 1.5},
        },
        # Valid configuration with TLS certificates instead of Let's Encrypt
        {
            "user_environment": {"default_app": "jupyterlab"},
            "https": {
                "enabled": True,
                "tls": {
                    "key": "/etc/tljh/tls/private.key",
                    "cert": "/etc/tljh/tls/certificate.crt",
                },
            },
        },
        # Valid configuration with TLS and custom HTTPS address/port
        {
            "user_environment": {"default_app": "jupyterlab"},
            "https": {
                "enabled": True,
                "address": "192.168.1.1",
                "port": 443,
                "tls": {
                    "key": "/etc/tljh/tls/private.key",
                    "cert": "/etc/tljh/tls/certificate.crt",
                },
            },
        },
    ],
)
def test_valid_configs(valid_config):
    """Test that known good configs pass validation without errors."""
    try:
        config.validate_config(valid_config, validate=True)
    except Exception as e:
        pytest.fail(f"Valid config failed validation: {e}")


@pytest.mark.parametrize(
    "invalid_config",
    [
        # Invalid default_app value
        {
            "user_environment": {"default_app": "saturnlab"},
            "https": {
                "enabled": True,
                "letsencrypt": {
                    "email": "admin@example.com",
                    "domains": ["sub.example.com"],
                },
            },
        },
        # Invalid domains type (should be array)
        {
            "user_environment": {"default_app": "jupyterlab"},
            "https": {
                "enabled": True,
                "letsencrypt": {"email": "not-an-email", "domains": "example.com"},
            },
        },
        # Extra unexpected property
        {
            "user_environment": {"default_app": "jupyterlab"},
            "https": {
                "enabled": True,
                "letsencrypt": {
                    "email": "admin@example.com",
                    "domains": ["example.com"],
                    "extra_property": "invalid",
                },
            },
        },
        # Invalid culling service config (timeout should be an integer)
        {
            "user_environment": {"default_app": "jupyterlab"},
            "https": {"enabled": False},
            "services": {
                "cull": {
                    "enabled": True,
                    "timeout": "one hour",
                    "every": 600,
                    "concurrency": 5,
                    "users": True,
                    "max_age": 86400,
                    "remove_named_servers": False,
                }
            },
        },
        # Invalid resource limits (negative CPU value)
        {
            "user_environment": {"default_app": "jupyterlab"},
            "https": {"enabled": False},
            "limits": {"memory": "2G", "cpu": -1},  # Negative CPU not allowed
        },
        # TLS enabled but missing required key
        {
            "user_environment": {"default_app": "jupyterlab"},
            "https": {
                "enabled": True,
                "tls": {
                    "cert": "/etc/tljh/tls/certificate.crt"
                    # Missing 'key' field
                },
            },
        },
        {
            "user_environment": {"default_app": "jupyterlab"},
            "https": {
                "enabled": True,
                "tls": {
                    "key": "/etc/tljh/tls/private.key"
                    # Missing 'cert' field
                },
            },
        },
    ],
)
def test_invalid_configs(invalid_config):
    """Test that known bad configs raise validation errors."""
    with pytest.raises(SystemExit) as exc_info:
        config.validate_config(invalid_config, validate=True)

    assert exc_info.value.code == 1
