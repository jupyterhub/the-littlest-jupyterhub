"""
Test conda commandline wrappers
"""
from tljh import conda
import os
import pytest
import subprocess
import tempfile


@pytest.fixture(scope='module')
def prefix():
    """
    Provide a temporary directory with a conda environment
    """
    miniconda_version = '4.7.10'
    miniconda_installer_sha256 = "8a324adcc9eaf1c09e22a992bb6234d91a94146840ee6b11c114ecadafc68121"
    installer_url = "https://repo.continuum.io/miniconda/Miniconda3-{}-Linux-x86_64.sh".format(miniconda_version)
    with tempfile.TemporaryDirectory() as tmpdir:
        with conda.download_miniconda_installer(installer_url, miniconda_installer_sha256) as installer_path:
            conda.install_miniconda(installer_path, tmpdir)
        conda.ensure_conda_packages(tmpdir, [
            'conda==4.8.1'
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
