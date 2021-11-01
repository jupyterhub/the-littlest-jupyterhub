"""tests for the proxy"""
import os
import shutil
import ssl
from subprocess import check_call
import time

import toml
from tornado.httpclient import HTTPClient, HTTPRequest, HTTPClientError
import pytest

from tljh.config import (
    reload_component,
    set_config_value,
    CONFIG_FILE,
    CONFIG_DIR,
    STATE_DIR,
)


def send_request(url, max_sleep, validate_cert=True, username=None, password=None):
    resp = None
    for i in range(max_sleep):
        time.sleep(i)
        try:
            req = HTTPRequest(
                url,
                method="GET",
                auth_username=username,
                auth_password=password,
                validate_cert=validate_cert,
                follow_redirects=True,
                max_redirects=15,
            )
            resp = HTTPClient().fetch(req)
            break
        except Exception as e:
            print(e)
            pass

    return resp


def test_manual_https(preserve_config):
    ssl_dir = "/etc/tljh-ssl-test"
    key = ssl_dir + "/ssl.key"
    cert = ssl_dir + "/ssl.cert"
    os.makedirs(ssl_dir, exist_ok=True)
    os.chmod(ssl_dir, 0o600)
    # generate key and cert
    check_call(
        [
            "openssl",
            "req",
            "-nodes",
            "-newkey",
            "rsa:2048",
            "-keyout",
            key,
            "-x509",
            "-days",
            "1",
            "-out",
            cert,
            "-subj",
            "/CN=tljh.jupyer.org",
        ]
    )
    set_config_value(CONFIG_FILE, "https.enabled", True)
    set_config_value(CONFIG_FILE, "https.tls.key", key)
    set_config_value(CONFIG_FILE, "https.tls.cert", cert)
    reload_component("proxy")
    for i in range(10):
        time.sleep(i)
        try:
            server_cert = ssl.get_server_certificate(("127.0.0.1", 443))
        except Exception as e:
            print(e)
        else:
            break
    with open(cert) as f:
        file_cert = f.read()

    # verify that our certificate was loaded by traefik
    assert server_cert == file_cert

    # verify that we can still connect to the hub
    resp = send_request(
        url="https://127.0.0.1/hub/api", max_sleep=10, validate_cert=False
    )
    assert resp.code == 200

    # cleanup
    shutil.rmtree(ssl_dir)
    set_config_value(CONFIG_FILE, "https.enabled", False)

    reload_component("proxy")


def test_extra_traefik_config():
    extra_static_config_dir = os.path.join(CONFIG_DIR, "traefik_config.d")
    os.makedirs(extra_static_config_dir, exist_ok=True)

    dynamic_config_dir = os.path.join(STATE_DIR, "rules")
    os.makedirs(dynamic_config_dir, exist_ok=True)

    extra_static_config = {
        "entryPoints": {"no_auth_api": {"address": "127.0.0.1:9999"}},
        "api": {"dashboard": True, "entrypoint": "no_auth_api"},
    }

    extra_dynamic_config = {
        "frontends": {
            "test": {
                "backend": "test",
                "routes": {
                    "rule1": {"rule": "PathPrefixStrip: /the/hub/runs/here/too"}
                },
            }
        },
        "backends": {
            # redirect to hub
            "test": {"servers": {"server1": {"url": "http://127.0.0.1:15001"}}}
        },
    }

    success = False
    for i in range(5):
        time.sleep(i)
        try:
            with pytest.raises(HTTPClientError, match="HTTP 401: Unauthorized"):
                # The default dashboard entrypoint requires authentication, so it should fail
                req = HTTPRequest("http://127.0.0.1:8099/dashboard/", method="GET")
                HTTPClient().fetch(req)
            success = True
            break
        except Exception as e:
            pass

    assert success == True

    # write the extra static config
    with open(
        os.path.join(extra_static_config_dir, "extra.toml"), "w+"
    ) as extra_config_file:
        toml.dump(extra_static_config, extra_config_file)

    # write the extra dynamic config
    with open(
        os.path.join(dynamic_config_dir, "extra_rules.toml"), "w+"
    ) as extra_config_file:
        toml.dump(extra_dynamic_config, extra_config_file)

    # load the extra config
    reload_component("proxy")

    # the new dashboard entrypoint shouldn't require authentication anymore
    resp = send_request(url="http://127.0.0.1:9999/dashboard/", max_sleep=5)
    assert resp.code == 200

    # test extra dynamic config
    resp = send_request(url="http://127.0.0.1/the/hub/runs/here/too", max_sleep=5)
    assert resp.code == 200
    assert "http://127.0.0.1/hub/login" in resp.effective_url

    # cleanup
    os.remove(os.path.join(extra_static_config_dir, "extra.toml"))
    os.remove(os.path.join(dynamic_config_dir, "extra_rules.toml"))
    open(os.path.join(STATE_DIR, "traefik.toml"), "w").close()
