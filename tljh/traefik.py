"""Traefik installation and setup"""
import hashlib
import os
from glob import glob

from jinja2 import Template
from passlib.apache import HtpasswdFile
import backoff
import requests
import toml

from .config import CONFIG_DIR
from tljh.configurer import load_config, _merge_dictionaries

# traefik 2.7.x is not supported yet, use v1.7.x for now
# see: https://github.com/jupyterhub/traefik-proxy/issues/97
machine = os.uname().machine
if machine == "aarch64":
    plat = "linux-arm64"
elif machine == "x86_64":
    plat = "linux-amd64"
else:
    raise OSError(f"Error. Platform: {os.uname().sysname} / {machine} Not supported.")
traefik_version = "1.7.33"

# record sha256 hashes for supported platforms here
checksums = {
    "linux-amd64": "314ffeaa4cd8ed6ab7b779e9b6773987819f79b23c28d7ab60ace4d3683c5935",
    "linux-arm64": "0640fa665125efa6b598fc08c100178e24de66c5c6035ce5d75668d3dc3706e1",
}


def checksum_file(path):
    """Compute the sha256 checksum of a path"""
    hasher = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def fatal_error(e):
    # Retry only when connection is reset or we think we didn't download entire file
    return str(e) != "ContentTooShort" and not isinstance(e, ConnectionResetError)


@backoff.on_exception(backoff.expo, Exception, max_tries=2, giveup=fatal_error)
def ensure_traefik_binary(prefix):
    """Download and install the traefik binary to a location identified by a prefix path such as '/opt/tljh/hub/'"""
    traefik_bin = os.path.join(prefix, "bin", "traefik")
    if os.path.exists(traefik_bin):
        checksum = checksum_file(traefik_bin)
        if checksum == checksums[plat]:
            # already have the right binary
            # ensure permissions and we're done
            os.chmod(traefik_bin, 0o755)
            return
        else:
            print(f"checksum mismatch on {traefik_bin}")
            os.remove(traefik_bin)

    traefik_url = (
        "https://github.com/containous/traefik/releases"
        f"/download/v{traefik_version}/traefik_{plat}"
    )

    print(f"Downloading traefik {traefik_version}...")
    # download the file
    response = requests.get(traefik_url)
    if response.status_code == 206:
        raise Exception("ContentTooShort")
    with open(traefik_bin, "wb") as f:
        f.write(response.content)
    os.chmod(traefik_bin, 0o755)

    # verify that we got what we expected
    checksum = checksum_file(traefik_bin)
    if checksum != checksums[plat]:
        raise OSError(f"Checksum failed {traefik_bin}: {checksum} != {checksums[plat]}")


def compute_basic_auth(username, password):
    """Generate hashed HTTP basic auth from traefik_api username+password"""
    ht = HtpasswdFile()
    # generate htpassword
    ht.set_password(username, password)
    hashed_password = str(ht.to_string()).split(":")[1][:-3]
    return username + ":" + hashed_password


def load_extra_config(extra_config_dir):
    extra_configs = sorted(glob(os.path.join(extra_config_dir, "*.toml")))
    # Load the toml list of files into dicts and merge them
    config = toml.load(extra_configs)
    return config


def ensure_traefik_config(state_dir):
    """Render the traefik.toml config file"""
    traefik_std_config_file = os.path.join(state_dir, "traefik.toml")
    traefik_extra_config_dir = os.path.join(CONFIG_DIR, "traefik_config.d")
    traefik_dynamic_config_dir = os.path.join(state_dir, "rules")

    config = load_config()
    config["traefik_api"]["basic_auth"] = compute_basic_auth(
        config["traefik_api"]["username"],
        config["traefik_api"]["password"],
    )

    with open(os.path.join(os.path.dirname(__file__), "traefik.toml.tpl")) as f:
        template = Template(f.read())
    std_config = template.render(config)
    https = config["https"]
    letsencrypt = https["letsencrypt"]
    tls = https["tls"]
    # validate https config
    if https["enabled"]:
        if not tls["cert"] and not letsencrypt["email"]:
            raise ValueError(
                "To enable https, you must set tls.cert+key or letsencrypt.email+domains"
            )
        if (letsencrypt["email"] and not letsencrypt["domains"]) or (
            letsencrypt["domains"] and not letsencrypt["email"]
        ):
            raise ValueError("Both email and domains must be set for letsencrypt")

    # Ensure traefik extra static config dir exists and is private
    os.makedirs(traefik_extra_config_dir, mode=0o700, exist_ok=True)

    # Ensure traefik dynamic config dir exists and is private
    os.makedirs(traefik_dynamic_config_dir, mode=0o700, exist_ok=True)

    try:
        # Load standard config file merge it with the extra config files into a dict
        extra_config = load_extra_config(traefik_extra_config_dir)
        new_toml = _merge_dictionaries(toml.loads(std_config), extra_config)
    except FileNotFoundError:
        new_toml = toml.loads(std_config)

    # Dump the dict into a toml-formatted string and write it to file
    with open(traefik_std_config_file, "w") as f:
        os.fchmod(f.fileno(), 0o600)
        toml.dump(new_toml, f)

    with open(os.path.join(traefik_dynamic_config_dir, "rules.toml"), "w") as f:
        os.fchmod(f.fileno(), 0o600)

    # ensure acme.json exists and is private
    with open(os.path.join(state_dir, "acme.json"), "a") as f:
        os.fchmod(f.fileno(), 0o600)
