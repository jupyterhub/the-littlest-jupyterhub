"""
Test conda commandline wrappers
"""
from tljh import conda
from tljh import installer
import os
import pytest
import subprocess
import tempfile


@pytest.fixture(scope="module")
def prefix():
    """
    Provide a temporary directory with a mambaforge conda environment
    """
    machine = os.uname().machine
    installer_url, checksum = installer._mambaforge_url()
    with tempfile.TemporaryDirectory() as tmpdir:
        with conda.download_miniconda_installer(
            installer_url, checksum
        ) as installer_path:
            conda.install_miniconda(installer_path, tmpdir)
        conda.ensure_conda_packages(
            tmpdir,
            [
                f"conda=={installer.MAMBAFORGE_CONDA_VERSION}",
                f"mamba=={installer.MAMBAFORGE_MAMBA_VERSION}",
            ],
        )
        yield tmpdir


def test_ensure_packages(prefix):
    """
    Test installing packages in conda environment
    """
    conda.ensure_conda_packages(prefix, ["numpy"])
    # Throws an error if this fails
    subprocess.check_call([os.path.join(prefix, "bin", "python"), "-c", "import numpy"])


def test_ensure_pip_packages(prefix):
    """
    Test installing pip packages in conda environment
    """
    conda.ensure_conda_packages(prefix, ["pip"])
    conda.ensure_pip_packages(prefix, ["numpy"])
    # Throws an error if this fails
    subprocess.check_call([os.path.join(prefix, "bin", "python"), "-c", "import numpy"])


def test_ensure_pip_requirements(prefix):
    """
    Test installing pip packages with requirements.txt in conda environment
    """
    conda.ensure_conda_packages(prefix, ["pip"])
    with tempfile.NamedTemporaryFile() as f:
        # Sample small package to test
        f.write(b"there")
        f.flush()
        conda.ensure_pip_requirements(prefix, f.name)
    subprocess.check_call([os.path.join(prefix, "bin", "python"), "-c", "import there"])
