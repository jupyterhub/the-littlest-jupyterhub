"""
Wrap conda commandline program
"""
import os
import subprocess
import json


def ensure_conda_env(prefix):
    """
    Ensure a conda environment in the prefix
    """
    abspath = os.path.abspath(prefix)
    try:
        output = json.loads(
            subprocess.check_output(['conda', 'create', '--json', '--prefix', abspath]).decode()
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
    raw_output = subprocess.check_output([
        'conda', 'install',
        '--json',
        '--prefix', abspath
    ] + packages).decode()
    # `conda install` outputs JSON lines for fetch updates,
    # and a undelimited output at the end. There is no reasonable way to
    # parse this outside of this kludge.
    filtered_output = '\n'.join([
        l for l in raw_output.split('\n')
        # Sometimes the JSON messages start with a \00. The lstrip removes these.
        if not l.lstrip().startswith('{"fetch"')
    ])
    output = json.loads(filtered_output)
    if 'success' in output and output['success'] == True:
        return
