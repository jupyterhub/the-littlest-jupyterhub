"""Traefik installation and setup"""

import hashlib
import io
import logging
import os
import tarfile
from glob import glob
from pathlib import Path
from subprocess import run

import backoff
import requests
import toml
from jinja2 import Template

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

# Traefik releases: https://github.com/traefik/traefik/releases
traefik_version = "3.1.4"

# record sha256 hashes for supported platforms here
# checksums are published in the checksums.txt of each release
checksums = {
    "linux_amd64": "eb7227b1b235195355904839c514a9ed6a0aecdcf5dab02ad48db21b05c5e700",
    "linux_arm64": "e5d970a7f11267b70a8e308cb80f859bba4f420f24789f7393fdf3f4cd031631",
}

_tljh_path = Path(__file__).parent.resolve()


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
        version_out = run(
            [traefik_bin, "version"],
            capture_output=True,
            text=True,
        ).stdout
    except (FileNotFoundError, OSError) as e:
        logger.debug(f"Failed to get traefik version: {e}")
        return False
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
    """
    Ensure that a traefik binary of a hardcoded version is made available at a
    prefix path such as '/opt/tljh/hub/'.
    """
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
        "https://github.com/traefik/traefik/releases"
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
    traefik_dynamic_config_file = os.path.join(
        traefik_dynamic_config_dir, "dynamic.toml"
    )

    config = load_config()
    config["traefik_dynamic_config_dir"] = traefik_dynamic_config_dir

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

    with (_tljh_path / "traefik.toml.tpl").open() as f:
        template = Template(f.read())
    std_config = template.render(config)

    with (_tljh_path / "traefik-dynamic.toml.tpl").open() as f:
        dynamic_template = Template(f.read())
    dynamic_config = dynamic_template.render(config)

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

    with open(os.path.join(traefik_dynamic_config_dir, "dynamic.toml"), "w") as f:
        os.fchmod(f.fileno(), 0o600)
        # validate toml syntax before writing
        toml.loads(dynamic_config)
        f.write(dynamic_config)

    with open(os.path.join(traefik_dynamic_config_dir, "rules.toml"), "w") as f:
        os.fchmod(f.fileno(), 0o600)

    # ensure acme.json exists and is private
    with open(os.path.join(state_dir, "acme.json"), "a") as f:
        os.fchmod(f.fileno(), 0o600)
