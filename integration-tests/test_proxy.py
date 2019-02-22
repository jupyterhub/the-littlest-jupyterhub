"""tests for the proxy"""
import os
import shutil
import ssl
from subprocess import check_call
import time

import requests

from tljh.config import reload_component, set_config_value, CONFIG_FILE


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

    for i in range(5):
        time.sleep(i)
        # verify that we can still connect to the hub
        r = requests.get("https://127.0.0.1/hub/api", verify=False)
        if r.status_code == 200:
            break;

    r.raise_for_status()

    # cleanup
    shutil.rmtree(ssl_dir)
