"""
Test conda commandline wrappers
"""
import os
import subprocess
import tempfile

import pytest

from tljh import conda


@pytest.fixture(scope='module')
def prefix():
    """
    Provide a temporary directory with a conda environment
    """
    mambaforge_version = '4.10.3-7'
    installer_sha256 = "fc872522ec427fcab10167a93e802efaf251024b58cc27b084b915a9a73c4474"
    installer_url = "https://github.com/conda-forge/miniforge/releases/download/{v}/Mambaforge-{v}-Linux-x86_64.sh".format(v=mambaforge_version)
    with tempfile.TemporaryDirectory() as tmpdir:
        with conda.download_miniconda_installer(installer_url, installer_sha256) as installer_path:
            conda.install_miniconda(installer_path, tmpdir)
        conda.ensure_conda_packages(tmpdir, [
            'conda==4.10.3'
        ])
        yield tmpdir


def test_ensure_packages(prefix):
    """
    Test installing packages in conda environment
    """
    conda.ensure_conda_packages(prefix, ['numpy'])
    # Throws an error if this fails
    subprocess.check_call([
        os.path.join(prefix, 'bin', 'python'),
        '-c',
        'import numpy'
    ])


def test_ensure_pip_packages(prefix):
    """
    Test installing pip packages in conda environment
    """
    conda.ensure_conda_packages(prefix, ['pip'])
    conda.ensure_pip_packages(prefix, ['numpy'])
    # Throws an error if this fails
    subprocess.check_call([
        os.path.join(prefix, 'bin', 'python'),
        '-c',
        'import numpy'
    ])


def test_ensure_pip_requirements(prefix):
    """
    Test installing pip packages with requirements.txt in conda environment
    """
    conda.ensure_conda_packages(prefix, ['pip'])
    with tempfile.NamedTemporaryFile() as f:
        # Sample small package to test
        f.write('there'.encode())
        f.flush()
        conda.ensure_pip_requirements(prefix, f.name)
    subprocess.check_call([
        os.path.join(prefix, 'bin', 'python'),
        '-c',
        'import there'
    ])
