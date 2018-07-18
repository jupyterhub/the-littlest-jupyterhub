"""
Test conda commandline wrappers
"""
from tljh import conda
import os
import pytest
import subprocess
import tempfile


@pytest.fixture
def prefix():
    """
    Provide a temporary directory to make environments in.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        yield tmpdir


def test_create_environment(prefix):
    """
    Test conda environment creation

    An empty conda environment doesn't seem to have anything in it,
    so we just check for directory existence.
    """
    conda.ensure_conda_env(prefix)
    assert os.path.exists(prefix)


def test_ensure_environment(prefix):
    """
    Test second call to ensure_conda_env works as expected

    A conda environment already exists, so we it should just do nothing
    """
    conda.ensure_conda_env(prefix)
    assert os.path.exists(prefix)
    conda.ensure_conda_env(prefix)


def test_ensure_packages(prefix):
    """
    Test installing packages in conda environment
    """
    conda.ensure_conda_env(prefix)
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
    conda.ensure_conda_env(prefix)
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
    conda.ensure_conda_env(prefix)
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
