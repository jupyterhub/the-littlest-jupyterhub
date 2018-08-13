import os
import subprocess


def test_serverextensions():
    """
    Validate serverextensions we want are installed
    """
    # jupyter-serverextension writes to stdout and stderr weirdly
    proc = subprocess.run([
        '/opt/tljh/user/bin/jupyter-serverextension',
        'list', '--sys-prefix'
    ], stderr=subprocess.PIPE)

    extensions = [
        'jupyterlab 0.32.1',
        'nbgitpuller 0.6.1',
        'nteract_on_jupyter 1.8.1',
        'nbresuse '
    ]

    for e in extensions:
        assert '{} \x1b[32mOK\x1b[0m'.format(e) in proc.stderr.decode()

def test_nbextensions():
    """
    Validate nbextensions we want are installed & enabled
    """
    # jupyter-nbextension writes to stdout and stderr weirdly
    proc = subprocess.run([
        '/opt/tljh/user/bin/jupyter-nbextension',
        'list', '--sys-prefix'
    ], stderr=subprocess.PIPE, stdout=subprocess.PIPE)

    extensions = [
        'nbresuse/main',
    ]

    for e in extensions:
        assert '{} \x1b[32m enabled \x1b[0m'.format(e) in proc.stdout.decode()

    # Ensure we have 'OK' messages in our stdout, to make sure everything is importable
    proc.stderr.decode() == '      - Validating: \x1b[32mOK\x1b[0m\n' * len(extensions)


def test_labextensions():
    """
    Validate labextensions we want installed
    """
    # Currently we only install jupyterhub
    assert os.path.exists('/opt/tljh/user/bin/jupyter-labhub')