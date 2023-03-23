"""
Unit test  functions in installer.py
"""
import json
import os
from unittest import mock
from subprocess import run, PIPE

import pytest

from tljh import conda
from tljh import installer
from tljh.utils import parse_version as V
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
    elif distro == "miniconda":
        arch = os.uname().machine
        installer_url = (
            f"https://repo.anaconda.com/miniconda/Miniconda3-{version}-Linux-{arch}.sh"
        )
    else:
        raise ValueError(f"{distro=} must be 'miniconda' or 'mambaforge'")
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


@pytest.mark.parametrize(
    "distro, version, conda_version, mamba_version",
    [
        (
            None,
            None,
            installer.MAMBAFORGE_CONDA_VERSION,
            installer.MAMBAFORGE_MAMBA_VERSION,
        ),
        (
            "exists",
            None,
            installer.MAMBAFORGE_CONDA_VERSION,
            installer.MAMBAFORGE_MAMBA_VERSION,
        ),
        (
            "mambaforge",
            "22.11.1-4",
            installer.MAMBAFORGE_CONDA_VERSION,
            installer.MAMBAFORGE_MAMBA_VERSION,
        ),
        ("mambaforge", "4.10.3-7", "4.10.3", "0.16.0"),
        (
            "miniconda",
            "4.7.10",
            installer.MAMBAFORGE_CONDA_VERSION,
            installer.MAMBAFORGE_MAMBA_VERSION,
        ),
        (
            "miniconda",
            "4.5.1",
            installer.MAMBAFORGE_CONDA_VERSION,
            installer.MAMBAFORGE_MAMBA_VERSION,
        ),
    ],
)
def test_ensure_user_environment(
    user_env_prefix,
    distro,
    version,
    conda_version,
    mamba_version,
):
    if version and V(version) < V("4.10.1") and os.uname().machine == "aarch64":
        pytest.skip(f"Miniconda {version} not available for aarch64")
    canary_file = user_env_prefix / "test-file.txt"
    canary_package = "types-backports_abc"
    if distro:
        if distro == "exists":
            user_env_prefix.mkdir()
        else:
            setup_conda(distro, version, user_env_prefix)
            # install a noarch: python package that won't be used otherwise
            # should depend on Python, so it will interact with possible upgrades
            run(
                [
                    str(user_env_prefix / "bin/conda"),
                    "install",
                    "-y",
                    "-c" "conda-forge",
                    canary_package,
                ],
                input="",
                check=True,
            )

        # make a file not managed by conda, to check for wipeouts
        with canary_file.open("w") as f:
            f.write("I'm here\n")

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
        if distro != "exists":
            # make sure we didn't delete the installed package
            assert canary_package in packages

    assert "conda" in packages
    assert packages["conda"]["version"] == conda_version
    assert "mamba" in packages
    assert packages["mamba"]["version"] == mamba_version
