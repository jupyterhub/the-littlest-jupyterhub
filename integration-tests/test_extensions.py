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
        'jupyterlab 1.2.1',
        'nbgitpuller 0.7.2',
        'nteract_on_jupyter 2.1.3',
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
        # This is what ipywidgets nbextension is called
        'jupyter-js-widgets/extension'
    ]

    for e in extensions:
        assert '{} \x1b[32m enabled \x1b[0m'.format(e) in proc.stdout.decode()

    # Ensure we have 'OK' messages in our stdout, to make sure everything is importable
    assert proc.stderr.decode() == '    - Validating: \x1b[32mOK\x1b[0m\n' * len(extensions)


def test_labextensions():
    """
    Validate labextensions we want installed
    """
    # Currently we only install jupyterhub
    assert os.path.exists('/opt/tljh/user/bin/jupyter-labhub')
