"""Test traefik configuration"""
import os

import pytest
import toml

from tljh import config, traefik


def test_download_traefik(tmpdir):
    traefik_bin = tmpdir.mkdir("bin").join("traefik")
    traefik.ensure_traefik_binary(str(tmpdir))
    assert traefik_bin.exists()
    # ignore higher-order permission bits, only verify ugo permissions
    assert (traefik_bin.stat().mode & 0o777) == 0o755


def _read_toml(path):
    """Read a toml file

    print config for debugging on failure
    """
    print(path)
    with open(path) as f:
        toml_cfg = f.read()
        print(toml_cfg)
        return toml.loads(toml_cfg)


def _read_static_config(state_dir):
    return _read_toml(os.path.join(state_dir, "traefik.toml"))


def _read_dynamic_config(state_dir):
    return _read_toml(os.path.join(state_dir, "rules", "dynamic.toml"))


def test_default_config(tmpdir, tljh_dir):
    state_dir = tmpdir.mkdir("state")
    traefik.ensure_traefik_config(str(state_dir))
    assert state_dir.join("traefik.toml").exists()
    os.path.join(state_dir, "traefik.toml")
    rules_dir = os.path.join(state_dir, "rules")

    cfg = _read_static_config(state_dir)
    assert cfg["api"] == {}
    assert cfg["entryPoints"] == {
        "http": {
            "address": ":80",
            "transport": {"respondingTimeouts": {"idleTimeout": "10m"}},
        },
        "auth_api": {
            "address": "localhost:8099",
        },
    }
    assert cfg["providers"] == {
        "providersThrottleDuration": "0s",
        "file": {"directory": rules_dir, "watch": True},
    }

    dynamic_config = _read_dynamic_config(state_dir)
    assert dynamic_config == {}


def test_letsencrypt_config(tljh_dir):
    state_dir = config.STATE_DIR
    config.set_config_value(config.CONFIG_FILE, "https.enabled", True)
    config.set_config_value(
        config.CONFIG_FILE, "https.letsencrypt.email", "fake@jupyter.org"
    )
    config.set_config_value(
        config.CONFIG_FILE, "https.letsencrypt.domains", ["testing.jovyan.org"]
    )
    traefik.ensure_traefik_config(str(state_dir))

    cfg = _read_static_config(state_dir)
    assert cfg["entryPoints"] == {
        "http": {
            "address": ":80",
            "http": {
                "redirections": {
                    "entryPoint": {
                        "scheme": "https",
                        "to": "https",
                    },
                },
            },
            "transport": {"respondingTimeouts": {"idleTimeout": "10m"}},
        },
        "https": {
            "address": ":443",
            "http": {"tls": {"options": "default"}},
            "transport": {"respondingTimeouts": {"idleTimeout": "10m"}},
        },
        "auth_api": {
            "address": "localhost:8099",
        },
    }
    assert "tls" not in cfg

    dynamic_config = _read_dynamic_config(state_dir)

    assert dynamic_config["tls"] == {
        "options": {
            "default": {
                "minVersion": "VersionTLS12",
                "cipherSuites": [
                    "TLS_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384",
                    "TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384",
                    "TLS_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256",
                    "TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256",
                    "TLS_ECDHE_ECDSA_WITH_CHACHA20_POLY1305",
                    "TLS_ECDHE_RSA_WITH_CHACHA20_POLY1305",
                ],
            }
        },
        "stores": {
            "default": {
                "defaultGeneratedCert": {
                    "resolver": "letsencrypt",
                    "domain": {
                        "main": "testing.jovyan.org",
                        "sans": [],
                    },
                }
            }
        },
    }
    assert "certificatesResolvers" in cfg
    assert "letsencrypt" in cfg["certificatesResolvers"]

    assert cfg["certificatesResolvers"]["letsencrypt"]["acme"] == {
        "email": "fake@jupyter.org",
        "storage": "acme.json",
        "tlsChallenge": {},
    }


def test_manual_ssl_config(tljh_dir):
    state_dir = config.STATE_DIR
    config.set_config_value(config.CONFIG_FILE, "https.enabled", True)
    config.set_config_value(config.CONFIG_FILE, "https.tls.key", "/path/to/ssl.key")
    config.set_config_value(config.CONFIG_FILE, "https.tls.cert", "/path/to/ssl.cert")
    traefik.ensure_traefik_config(str(state_dir))

    cfg = _read_static_config(state_dir)

    assert cfg["entryPoints"] == {
        "http": {
            "address": ":80",
            "http": {
                "redirections": {
                    "entryPoint": {
                        "scheme": "https",
                        "to": "https",
                    },
                },
            },
            "transport": {
                "respondingTimeouts": {
                    "idleTimeout": "10m",
                }
            },
        },
        "https": {
            "address": ":443",
            "http": {"tls": {"options": "default"}},
            "transport": {"respondingTimeouts": {"idleTimeout": "10m"}},
        },
        "auth_api": {
            "address": "localhost:8099",
        },
    }
    assert "tls" not in cfg

    dynamic_config = _read_dynamic_config(state_dir)

    assert "tls" in dynamic_config

    assert dynamic_config["tls"] == {
        "options": {
            "default": {
                "minVersion": "VersionTLS12",
                "cipherSuites": [
                    "TLS_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384",
                    "TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384",
                    "TLS_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256",
                    "TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256",
                    "TLS_ECDHE_ECDSA_WITH_CHACHA20_POLY1305",
                    "TLS_ECDHE_RSA_WITH_CHACHA20_POLY1305",
                ],
            },
        },
        "stores": {
            "default": {
                "defaultCertificate": {
                    "certFile": "/path/to/ssl.cert",
                    "keyFile": "/path/to/ssl.key",
                }
            }
        },
    }


def test_extra_config(tmpdir, tljh_dir):
    extra_config_dir = os.path.join(tljh_dir, config.CONFIG_DIR, "traefik_config.d")
    state_dir = tmpdir.mkdir("state")
    traefik_toml = os.path.join(state_dir, "traefik.toml")

    # Generate default config
    traefik.ensure_traefik_config(str(state_dir))

    # Read the default config
    toml_cfg = toml.load(traefik_toml)

    # Make sure the defaults are what we expect
    assert toml_cfg["log"]["level"] == "INFO"
    with pytest.raises(KeyError):
        toml_cfg["api"]["dashboard"]
    assert toml_cfg["entryPoints"]["auth_api"]["address"] == "localhost:8099"

    extra_config = {
        # modify existing value
        "log": {
            "level": "ERROR",
        },
        # add new setting
        "api": {"dashboard": True},
    }

    with open(os.path.join(extra_config_dir, "extra.toml"), "w+") as extra_config_file:
        toml.dump(extra_config, extra_config_file)

    # Merge the extra config with the defaults
    traefik.ensure_traefik_config(str(state_dir))

    # Read back the merged config
    toml_cfg = toml.load(traefik_toml)

    # Check that the defaults were updated by the extra config
    assert toml_cfg["log"]["level"] == "ERROR"
    assert toml_cfg["api"]["dashboard"] == True


def test_listen_address(tmpdir, tljh_dir):
    state_dir = config.STATE_DIR
    config.set_config_value(config.CONFIG_FILE, "http.address", "127.0.0.1")
    config.set_config_value(config.CONFIG_FILE, "https.address", "127.0.0.1")
    traefik.ensure_traefik_config(str(state_dir))

    cfg = _read_static_config(state_dir)
    assert cfg["entryPoints"]['http']['address'] == "127.0.0.1:80"
    assert cfg["entryPoints"]['https']['address'] == "127.0.0.1:443"
