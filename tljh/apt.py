"""
Utilities for working with the apt package manager
"""
import os
import subprocess
from tljh import utils


def trust_gpg_key(key):
    """
    Trust given GPG public key.

    key is a GPG public key (bytes) that can be passed to apt-key add via stdin.
    """
    # If gpg2 doesn't exist, install it.
    if not os.path.exists("/usr/bin/gpg2"):
        install_packages(["gnupg2"])
    utils.run_subprocess(["apt-key", "add", "-"], input=key)


def add_source(name, source_url, section):
    """
    Add a debian package source.

    distro is determined from /etc/os-release
    """
    # lsb_release is not installed in most docker images by default
    distro = (
        subprocess.check_output(
            ["/bin/bash", "-c", "source /etc/os-release && echo ${VERSION_CODENAME}"],
            stderr=subprocess.STDOUT,
        )
        .decode()
        .strip()
    )
    line = f"deb {source_url} {distro} {section}\n"
    with open(os.path.join("/etc/apt/sources.list.d/", name + ".list"), "a+") as f:
        # Write out deb line only if it already doesn't exist
        f.seek(0)
        if line not in f.read():
            f.write(line)
            f.truncate()
            utils.run_subprocess(["apt-get", "update", "--yes"])


def install_packages(packages):
    """
    Install debian packages
    """
    # Check if an apt-get update is required
    if len(os.listdir("/var/lib/apt/lists")) == 0:
        utils.run_subprocess(["apt-get", "update", "--yes"])
    env = os.environ.copy()
    # Stop apt from asking questions!
    env["DEBIAN_FRONTEND"] = "noninteractive"
    utils.run_subprocess(["apt-get", "install", "--yes"] + packages, env=env)
