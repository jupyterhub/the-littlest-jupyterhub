"""Traefik installation and setup"""
import hashlib
import io
import logging
import os
import tarfile
from glob import glob
from subprocess import run

import backoff
import requests
import toml
from jinja2 import Template
from passlib.apache import HtpasswdFile

from tljh.configurer import _merge_dictionaries, load_config

from .config import CONFIG_DIR

logger = logging.getLogger("tljh")

machine = os.uname().machine
if machine == "aarch64":
    plat = "linux_arm64"
elif machine == "x86_64":
    plat = "linux_amd64"
else:
    plat = None

traefik_version = "2.9.9"

# record sha256 hashes for supported platforms here
checksums = {
    "linux_amd64": "141db1434ae76890915486a4bc5ecf3dbafc8ece78984ce1a8db07737c42db88",
    "linux_arm64": "0a65ead411307669916ba629fa13f698acda0b2c5387abe0309b43e168e4e57f",
}


def checksum_file(path_or_file):
    """Compute the sha256 checksum of a path"""
    hasher = hashlib.sha256()
    if hasattr(path_or_file, "read"):
        f = path_or_file
    else:
        f = open(path_or_file, "rb")
    with f:
        for chunk in iter(lambda: f.read(4096), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def fatal_error(e):
    # Retry only when connection is reset or we think we didn't download entire file
    return str(e) != "ContentTooShort" and not isinstance(e, ConnectionResetError)


def check_traefik_version(traefik_bin):
    """Check the traefik version from `traefik version` output"""

    try:
        version_out = run([traefik_bin, "version"], capture=True, text=True)
    except (FileNotFoundError, OSError) as e:
        logger.debug(f"Failed to get traefik version: {e}")
        return False
    versions = {}
    for line in version_out.splitlines():
        before, _, after = line.partition(":")
        key = before.strip()
        if key.lower() == "version":
            version = after.strip()
            if version == traefik_version:
                logger.debug(f"Found {traefik_bin} {version}")
                return True
            else:
                logger.info(
                    f"Found {traefik_bin} version {version} != {traefik_version}"
                )
                return False

    logger.debug(f"Failed to extract traefik version from: {version_out}")
    return False


@backoff.on_exception(backoff.expo, Exception, max_tries=2, giveup=fatal_error)
def ensure_traefik_binary(prefix):
    """Download and install the traefik binary to a location identified by a prefix path such as '/opt/tljh/hub/'"""
    if plat is None:
        raise OSError(
            f"Error. Platform: {os.uname().sysname} / {machine} Not supported."
        )
    traefik_bin_dir = os.path.join(prefix, "bin")
    traefik_bin = os.path.join(prefix, "bin", "traefik")
    if os.path.exists(traefik_bin):
        if check_traefik_version(traefik_bin):
            return
        else:
            os.remove(traefik_bin)

    traefik_url = (
        "https://github.com/containous/traefik/releases"
        f"/download/v{traefik_version}/traefik_v{traefik_version}_{plat}.tar.gz"
    )

    logger.info(f"Downloading traefik {traefik_version} from {traefik_url}...")
    # download the file
    response = requests.get(traefik_url)
    response.raise_for_status()
    if response.status_code == 206:
        raise Exception("ContentTooShort")

    # verify that we got what we expected
    checksum = checksum_file(io.BytesIO(response.content))
    if checksum != checksums[plat]:
        raise OSError(f"Checksum failed {traefik_url}: {checksum} != {checksums[plat]}")

    with tarfile.open(fileobj=io.BytesIO(response.content)) as tf:
        tf.extract("traefik", path=traefik_bin_dir)
    os.chmod(traefik_bin, 0o755)


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
