"""
Wrap conda commandline program
"""
import os
import subprocess
import json
import hashlib
import contextlib
import tempfile
import requests
from distutils.version import LooseVersion as V
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


def check_miniconda_version(prefix, version):
    """
    Return true if a miniconda install with version exists at prefix
    """
    try:
        installed_version = (
            subprocess.check_output(
                [os.path.join(prefix, "bin", "conda"), "-V"], stderr=subprocess.STDOUT
            )
            .decode()
            .strip()
            .split()[1]
        )
        return V(installed_version) >= V(version)
    except (subprocess.CalledProcessError, FileNotFoundError):
        # Conda doesn't exist
        return False


@contextlib.contextmanager
def download_miniconda_installer(installer_url, sha256sum):
    """
    Context manager to download miniconda installer from a given URL

    This should be used as a contextmanager. It downloads miniconda installer
    of given version, verifies the sha256sum & provides path to it to the `with`
    block to run.
    """
    with tempfile.NamedTemporaryFile("wb") as f:
        f.write(requests.get(installer_url).content)
        # Remain in the NamedTemporaryFile context, but flush changes, see:
        # https://docs.python.org/3/library/os.html#os.fsync
        f.flush()
        os.fsync(f.fileno())

        if sha256_file(f.name) != sha256sum:
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


def ensure_conda_packages(prefix, packages):
    """
    Ensure packages (from conda-forge) are installed in the conda prefix.

    Note that conda seem to update dependencies by default, so there is probably
    no need to have a update parameter exposed for this function.
    """
    conda_executable = [os.path.join(prefix, "bin", "mamba")]
    abspath = os.path.abspath(prefix)
    # Let subprocess errors propagate
    # Explicitly do *not* capture stderr, since that's not always JSON!
    # Scripting conda is a PITA!
    # FIXME: raise different exception when using
    raw_output = subprocess.check_output(
        conda_executable
        + [
            "install",
            "-c",
            "conda-forge",  # Make customizable if we ever need to
            "--json",
            "--prefix",
            abspath,
        ]
        + packages
    ).decode()
    # `conda install` outputs JSON lines for fetch updates,
    # and a undelimited output at the end. There is no reasonable way to
    # parse this outside of this kludge.
    filtered_output = "\n".join(
        [
            l
            for l in raw_output.split("\n")
            # Sometimes the JSON messages start with a \x00. The lstrip removes these.
            # conda messages seem to randomly throw \x00 in places for no reason
            if not l.lstrip("\x00").startswith('{"fetch"')
        ]
    )
    output = json.loads(filtered_output.lstrip("\x00"))
    if "success" in output and output["success"] == True:
        return
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
