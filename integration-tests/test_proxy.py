"""tests for the proxy"""
import os
import shutil
import ssl
from subprocess import check_call
import time

import toml
from tornado.httpclient import HTTPClient, HTTPRequest, HTTPClientError
import pytest

from tljh.config import reload_component, set_config_value, CONFIG_FILE, CONFIG_DIR


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

    for i in range(10):
        time.sleep(i)
        # verify that we can still connect to the hub
        try:
            req = HTTPRequest(
                "https://127.0.0.1/hub/api", method="GET", validate_cert=False
            )
            resp = HTTPClient().fetch(req)
            break
        except Exception as e:
            pass
    assert resp.code == 200

    # cleanup
    shutil.rmtree(ssl_dir)


def test_extra_traefik_config():
    extra_config_dir = os.path.join(CONFIG_DIR, "traefik_config.d")
    os.makedirs(extra_config_dir, exist_ok=True)

    extra_config = {
        "entryPoints": {"no_auth_api": {"address": "127.0.0.1:9999"}},
        "api": {"dashboard": True, "entrypoint": "no_auth_api"},
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

    # Load the extra config
    with open(os.path.join(extra_config_dir, "extra.toml"), "w+") as extra_config_file:
        toml.dump(extra_config, extra_config_file)
    reload_component("proxy")

    for i in range(5):
        time.sleep(i)
        try:
            # The new dashboard entrypoint shouldn't require authentication anymore
            req = HTTPRequest("http://127.0.0.1:9999/dashboard/", method="GET")
            resp = HTTPClient().fetch(req)
            break
        except ConnectionRefusedError:
            pass
    # If the request didn't get through after 5 tries, this should fail
    assert resp.code == 200

    # cleanup
    os.remove(os.path.join(extra_config_dir, "extra.toml"))
    reload_component("proxy")
