"""
Unit test  functions in installer.py
"""

import json
import os
from subprocess import PIPE, run
from unittest import mock

import pytest
from packaging.specifiers import SpecifierSet
from packaging.version import parse as V

from tljh import conda, installer
from tljh.yaml import yaml


def test_ensure_config_yaml(tljh_dir):
    pm = installer.setup_plugins()
    installer.ensure_config_yaml(pm)
    assert os.path.exists(installer.CONFIG_FILE)
    assert os.path.isdir(installer.CONFIG_DIR)
    assert os.path.isdir(os.path.join(installer.CONFIG_DIR, "jupyterhub_config.d"))
    # verify that old config doesn't exist
    assert not os.path.exists(os.path.join(tljh_dir, "config.yaml"))


@pytest.mark.parametrize(
    "admins, expected_config",
    [
        ([["a1"], ["a2"], ["a3"]], ["a1", "a2", "a3"]),
        ([["a1:p1"], ["a2"]], ["a1", "a2"]),
    ],
)
def test_ensure_admins(tljh_dir, admins, expected_config):
    # --admin option called multiple times on the installer
    # creates a list of argument lists.
    installer.ensure_admins(admins)

    config_path = installer.CONFIG_FILE
    with open(config_path) as f:
        config = yaml.load(f)

    # verify the list was flattened
    assert config["users"]["admin"] == expected_config


def setup_conda(distro, version, prefix):
    """Install mambaforge or miniconda in a prefix"""
    if distro == "mambaforge":
        installer_url, _ = installer._mambaforge_url(version)
    elif distro == "miniforge":
        installer_url, _ = installer._mambaforge_url(version)
        installer_url = installer_url.replace("Mambaforge", "Miniforge3")
    elif distro == "miniconda":
        arch = os.uname().machine
        installer_url = (
            f"https://repo.anaconda.com/miniconda/Miniconda3-{version}-Linux-{arch}.sh"
        )
    else:
        raise ValueError(
            f"{distro=} must be 'miniconda' or 'mambaforge' or 'miniforge'"
        )
    with conda.download_miniconda_installer(installer_url, None) as installer_path:
        conda.install_miniconda(installer_path, str(prefix))
    # avoid auto-updating conda when we install other packages
    run(
        [
            str(prefix / "bin/conda"),
            "config",
            "--system",
            "--set",
            "auto_update_conda",
            "false",
        ],
        input="",
        check=True,
    )


@pytest.fixture
def user_env_prefix(tmp_path):
    user_env_prefix = tmp_path / "user_env"
    with mock.patch.object(installer, "USER_ENV_PREFIX", str(user_env_prefix)):
        yield user_env_prefix


def _specifier(version):
    """Convert version string to SpecifierSet

    If just a version number, add == to make it a specifier

    Any missing fields are replaced with .*

    If it's already a specifier string, pass it directly to SpecifierSet

    e.g.

    - 3.7 -> ==3.7.*
    - 1.2.3 -> ==1.2.3
    """
    if version[0].isdigit():
        # it's a version number, not a specifier
        if version.count(".") < 2:
            # pad missing fields
            version += ".*"
        version = f"=={version}"
    return SpecifierSet(version)


@pytest.mark.parametrize(
    # - distro: None, mambaforge, or miniforge
    # - distro_version: https://github.com/conda-forge/miniforge/releases
    # - expected_versions: versions of python, conda, and mamba in user env
    #
    # TLJH of a specific version comes with a specific distro_version as
    # declared in installer.py's MAMBAFORGE_VERSION variable, and it comes with
    # python, conda, and mamba of certain versions.
    #
    "distro, distro_version, expected_versions",
    [
        # No previous install, start fresh
        (
            None,
            None,
            {
                "python": "3.10.*",
                "conda": "23.1.0",
                "mamba": "1.4.1",
            },
        ),
        # previous install, 1.0
        (
            "mambaforge",
            "23.1.0-1",
            {
                "python": "3.10.*",
                "conda": "23.1.0",
                "mamba": "1.4.1",
            },
        ),
        # 0.2 install, no upgrade needed
        (
            "mambaforge",
            "4.10.3-7",
            {
                "python": "3.9.*",
                "conda": "4.10.3",
                "mamba": "0.16.0",
            },
        ),
        # simulate missing mamba
        # will be installed but not pinned
        # to avoid conflicts
        (
            "miniforge",
            "4.10.3-7",
            {
                "python": "3.9.*",
                "conda": "4.10.3",
                "mamba": ">=1.1.0",
            },
        ),
        # too-old Python (3.7), abort
        (
            "miniconda",
            "4.7.10",
            ValueError,
        ),
    ],
)
def test_ensure_user_environment(
    user_env_prefix,
    distro,
    distro_version,
    expected_versions,
):
    if (
        distro_version
        and V(distro_version) < V("4.10.1")
        and os.uname().machine == "aarch64"
    ):
        pytest.skip(f"{distro} {distro_version} not available for aarch64")
    canary_file = user_env_prefix / "test-file.txt"
    canary_package = "types-backports_abc"
    if distro:
        setup_conda(distro, distro_version, user_env_prefix)
        # install a noarch: python package that won't be used otherwise
        # should depend on Python, so it will interact with possible upgrades
        pkgs = [canary_package]
        run(
            [
                str(user_env_prefix / "bin/conda"),
                "install",
                "-S",
                "-y",
                "-c",
                "conda-forge",
            ]
            + pkgs,
            input="",
            check=True,
        )

        # make a file not managed by conda, to check for wipeouts
        with canary_file.open("w") as f:
            f.write("I'm here\n")

    if isinstance(expected_versions, type) and issubclass(expected_versions, Exception):
        exc_class = expected_versions
        with pytest.raises(exc_class):
            installer.ensure_user_environment("")
        return
    else:
        installer.ensure_user_environment("")

    p = run(
        [str(user_env_prefix / "bin/conda"), "list", "--json"],
        stdout=PIPE,
        text=True,
        check=True,
    )
    package_list = json.loads(p.stdout)
    packages = {package["name"]: package for package in package_list}

    if distro:
        # make sure we didn't wipe out files
        assert canary_file.exists()
        # make sure we didn't delete the installed package
        assert canary_package in packages

    for pkg, version in expected_versions.items():
        assert pkg in packages
        assert V(packages[pkg]["version"]) in _specifier(version)


def test_ensure_user_environment_no_clobber(user_env_prefix):
    # don't clobber existing user-env dir if it's non-empty and not a conda install
    user_env_prefix.mkdir()
    canary_file = user_env_prefix / "test-file.txt"
    with canary_file.open("w") as f:
        pass
    with pytest.raises(OSError):
        installer.ensure_user_environment("")
