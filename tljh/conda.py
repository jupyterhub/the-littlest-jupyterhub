"""
Wrap conda commandline program
"""
import contextlib
import hashlib
import json
import logging
import os
import subprocess
import tempfile
import time

import requests

from tljh import utils


def sha256_file(fname):
    """
    Return sha256 of a given filename

    Copied from https://stackoverflow.com/a/3431838
    """
    hash_sha256 = hashlib.sha256()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_sha256.update(chunk)
    return hash_sha256.hexdigest()


def get_conda_package_versions(prefix):
    """Get conda package versions, via `conda list --json`"""
    versions = {}
    try:
        out = subprocess.check_output(
            [os.path.join(prefix, "bin", "conda"), "list", "--json"],
            text=True,
        )
    except (subprocess.CalledProcessError, FileNotFoundError):
        return versions

    packages = json.loads(out)
    for package in packages:
        versions[package["name"]] = package["version"]
    return versions


@contextlib.contextmanager
def download_miniconda_installer(installer_url, sha256sum):
    """
    Context manager to download miniconda installer from a given URL

    This should be used as a contextmanager. It downloads miniconda installer
    of given version, verifies the sha256sum & provides path to it to the `with`
    block to run.
    """
    logger = logging.getLogger("tljh")
    logger.info(f"Downloading conda installer {installer_url}")
    with tempfile.NamedTemporaryFile("wb", suffix=".sh") as f:
        tic = time.perf_counter()
        r = requests.get(installer_url)
        r.raise_for_status()
        f.write(r.content)
        # Remain in the NamedTemporaryFile context, but flush changes, see:
        # https://docs.python.org/3/library/os.html#os.fsync
        f.flush()
        os.fsync(f.fileno())
        t = time.perf_counter() - tic
        logger.info(f"Downloaded conda installer {installer_url} in {t:.1f}s")

        if sha256sum and sha256_file(f.name) != sha256sum:
            raise Exception("sha256sum hash mismatch! Downloaded file corrupted")

        yield f.name


def fix_permissions(prefix):
    """Fix permissions in the install prefix

    For all files in the prefix, ensure that:
    - everything is owned by current user:group
    - nothing is world-writeable

    Run after each install command.
    """
    utils.run_subprocess(["chown", "-R", f"{os.getuid()}:{os.getgid()}", prefix])
    utils.run_subprocess(["chmod", "-R", "o-w", prefix])


def install_miniconda(installer_path, prefix):
    """
    Install miniconda with installer at installer_path under prefix
    """
    utils.run_subprocess(["/bin/bash", installer_path, "-u", "-b", "-p", prefix])
    # fix permissions on initial install
    # a few files have the wrong ownership and permissions initially
    # when the installer is run as root
    fix_permissions(prefix)


def ensure_conda_packages(prefix, packages, channels=('conda-forge',), force_reinstall=False):
    """
    Ensure packages (from channels) are installed in the conda prefix.

    Note that conda seem to update dependencies by default, so there is probably
    no need to have a update parameter exposed for this function.
    """
    conda_executable = os.path.join(prefix, "bin", "mamba")
    if not os.path.isfile(conda_executable):
        # fallback on conda if mamba is not present (e.g. for mamba to install itself)
        conda_executable = os.path.join(prefix, "bin", "conda")

    cmd = [conda_executable, "install", "--yes"]

    if force_reinstall:
        # use force-reinstall, e.g. for conda/mamba to ensure everything is okay
        # avoids problems with RemoveError upgrading conda from old versions
        cmd += ["--force-reinstall"]

    for channel in channels:
        cmd += ["-c", channel]

    abspath = os.path.abspath(prefix)

    utils.run_subprocess(
        cmd
        + [
            "--prefix",
            abspath,
        ]
        + packages,
        input="",
    )
    fix_permissions(prefix)


def ensure_pip_packages(prefix, packages, upgrade=False):
    """
    Ensure pip packages are installed in the given conda prefix.
    """
    abspath = os.path.abspath(prefix)
    pip_executable = [os.path.join(abspath, "bin", "python"), "-m", "pip"]
    pip_cmd = pip_executable + ["install"]
    if upgrade:
        pip_cmd.append("--upgrade")
    utils.run_subprocess(pip_cmd + packages)
    fix_permissions(prefix)


def ensure_pip_requirements(prefix, requirements_path, upgrade=False):
    """
    Ensure pip packages from given requirements_path are installed in given conda prefix.

    requirements_path can be a file or a URL.
    """
    abspath = os.path.abspath(prefix)
    pip_executable = [os.path.join(abspath, "bin", "python"), "-m", "pip"]
    pip_cmd = pip_executable + ["install"]
    if upgrade:
        pip_cmd.append("--upgrade")
    utils.run_subprocess(pip_cmd + ["--requirement", requirements_path])
    fix_permissions(prefix)
