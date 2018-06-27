"""
Wrap conda commandline program
"""
import os
import subprocess
import json
import sys

# Use sys.executable to call conda to avoid needing to fudge PATH
CONDA_EXECUTABLE = [sys.executable, '-m', 'conda']


def ensure_conda_env(prefix):
    """
    Ensure a conda environment in the prefix
    """
    abspath = os.path.abspath(prefix)
    try:
        output = json.loads(
            subprocess.check_output(CONDA_EXECUTABLE + ['create', '--json', '--prefix', abspath]).decode()
        )
    except subprocess.CalledProcessError as e:
        output = json.loads(e.output.decode())
        if 'error' in output and output['error'] == f'CondaValueError: prefix already exists: {abspath}':
            return
        raise
    if 'success' in output and output['success'] == True:
        return


def ensure_conda_packages(prefix, packages):
    """
    Ensure packages are installed in the conda prefix.
    """
    abspath = os.path.abspath(prefix)
    # Let subprocess errors propagate
    # FIXME: raise different exception when using
    raw_output = subprocess.check_output(CONDA_EXECUTABLE + [
        'install',
        '--json',
        '--prefix', abspath
    ] + packages).decode()
    # `conda install` outputs JSON lines for fetch updates,
    # and a undelimited output at the end. There is no reasonable way to
    # parse this outside of this kludge.
    filtered_output = '\n'.join([
        l for l in raw_output.split('\n')
        # Sometimes the JSON messages start with a \x00. The lstrip removes these.
        # conda messages seem to randomly throw \x00 in places for no reason
        if not l.lstrip('\x00').startswith('{"fetch"')
    ])
    output = json.loads(filtered_output.lstrip('\x00'))
    if 'success' in output and output['success'] == True:
        return


def ensure_pip_packages(prefix, packages):
    """
    Ensure pip packages are installed in the given conda prefix.
    """
    abspath = os.path.abspath(prefix)
    pip_executable = [os.path.join(abspath, 'bin', 'python'), '-m', 'pip']

    subprocess.check_output(pip_executable + [
        'install',
        '--no-cache-dir',
    ] + packages)
