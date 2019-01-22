"""Test traefik configuration"""
import os

import pytoml as toml

from tljh import config
from tljh import traefik


def test_download_traefik(tmpdir):
    traefik_bin = tmpdir.mkdir("bin").join("traefik")
    traefik.ensure_traefik_binary(str(tmpdir))
    assert traefik_bin.exists()
    # ignore higher-order permission bits, only verify ugo permissions
    assert (traefik_bin.stat().mode & 0o777) == 0o755


def test_default_config(tmpdir, tljh_dir):
    state_dir = tmpdir.mkdir("state")
    traefik.ensure_traefik_config(str(state_dir))
    assert state_dir.join("traefik.toml").exists()
    traefik_toml = os.path.join(state_dir, "traefik.toml")
    with open(traefik_toml) as f:
        toml_cfg = f.read()
        # print config for debugging on failure
        print(config.CONFIG_FILE)
        print(toml_cfg)
        cfg = toml.loads(toml_cfg)
    assert cfg["defaultEntryPoints"] == ["http"]
    assert cfg["entryPoints"] == {
        "http": {"address": ":80"},
        "auth_api": {
            "address": ":8099",
            "auth": {
                "basic": {"users": ["api_admin:$apr1$eS/j3kum$q/X2khsIEG/bBGsteP.x./"]}
            },
        },
    }


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
    traefik_toml = os.path.join(state_dir, "traefik.toml")
    with open(traefik_toml) as f:
        toml_cfg = f.read()
        # print config for debugging on failure
        print(config.CONFIG_FILE)
        print(toml_cfg)
        cfg = toml.loads(toml_cfg)
    assert cfg["defaultEntryPoints"] == ["http", "https"]
    assert "acme" in cfg
    assert cfg["entryPoints"] == {
        "http": {"address": ":80", "redirect": {"entryPoint": "https"}},
        "https": {"address": ":443", "tls": {}},
        "auth_api": {
            "address": ":8099",
            "auth": {
                "basic": {"users": ["api_admin:$apr1$eS/j3kum$q/X2khsIEG/bBGsteP.x./"]}
            },
        },
    }
    assert cfg["acme"] == {
        "email": "fake@jupyter.org",
        "storage": "acme.json",
        "entryPoint": "https",
        "httpChallenge": {"entryPoint": "http"},
        "domains": [{"main": "testing.jovyan.org"}],
    }


def test_manual_ssl_config(tljh_dir):
    state_dir = config.STATE_DIR
    config.set_config_value(config.CONFIG_FILE, "https.enabled", True)
    config.set_config_value(config.CONFIG_FILE, "https.tls.key", "/path/to/ssl.key")
    config.set_config_value(config.CONFIG_FILE, "https.tls.cert", "/path/to/ssl.cert")
    traefik.ensure_traefik_config(str(state_dir))
    traefik_toml = os.path.join(state_dir, "traefik.toml")
    with open(traefik_toml) as f:
        toml_cfg = f.read()
        # print config for debugging on failure
        print(config.CONFIG_FILE)
        print(toml_cfg)
        cfg = toml.loads(toml_cfg)
    assert cfg["defaultEntryPoints"] == ["http", "https"]
    assert "acme" not in cfg
    assert cfg["entryPoints"] == {
        "http": {"address": ":80", "redirect": {"entryPoint": "https"}},
        "https": {
            "address": ":443",
            "tls": {
                "certificates": [
                    {"certFile": "/path/to/ssl.cert", "keyFile": "/path/to/ssl.key"}
                ]
            },
        },
        "auth_api": {
            "address": ":8099",
            "auth": {
                "basic": {"users": ["api_admin:$apr1$eS/j3kum$q/X2khsIEG/bBGsteP.x./"]}
            },
        },
    }
