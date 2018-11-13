"""
Bootstrap an installation of TLJH.

Sets up just enough TLJH environments to invoke tljh.installer.

This script is run as:

    curl <script-url> | sudo python3 -

Constraints:
  - Entire script should be compatible with Python 3.6 (We run on Ubuntu 18.04+)
  - Script should parse in Python 3.4 (since we exit with useful error message on Ubuntu 14.04+)
  - Use stdlib modules only
"""
import os
import subprocess
import sys
import logging


def get_os_release_variable(key):
    """
    Return value for key from /etc/os-release

    /etc/os-release is a bash file, so should use bash to parse it.

    Returns empty string if key is not found.
    """
    return subprocess.check_output([
        '/bin/bash', '-c',
        "source /etc/os-release && echo ${{{key}}}".format(key=key)
    ]).decode().strip()

def main():

    # Support only Ubuntu 18.04+
    distro = get_os_release_variable('ID')
    version = float(get_os_release_variable('VERSION_ID'))
    if distro != 'ubuntu':
        print('The Littlest JupyterHub currently supports Ubuntu Linux only')
        sys.exit(1)
    elif float(version) < 18.04:
        print('The Littlest JupyterHub requires Ubuntu 18.04 or higher')
        sys.exit(1)

    install_prefix = os.environ.get('TLJH_INSTALL_PREFIX', '/opt/tljh')
    hub_prefix = os.path.join(install_prefix, 'hub')

    # Set up logging to print to a file and to stderr
    logger = logging.getLogger(__name__)

    os.makedirs(install_prefix, exist_ok=True)
    file_logger = logging.FileHandler(os.path.join(install_prefix, 'installer.log'))
    file_logger.setFormatter(logging.Formatter('%(asctime)s %(message)s'))
    logger.addHandler(file_logger)

    stderr_logger = logging.StreamHandler()
    stderr_logger.setFormatter(logging.Formatter('%(message)s'))
    logger.addHandler(stderr_logger)
    logger.setLevel(logging.INFO)

    logger.info('Checking if TLJH is already installed...')
    if os.path.exists(os.path.join(hub_prefix, 'bin', 'python3')):
        logger.info('TLJH already installed, upgrading...')
        initial_setup = False
    else:
        logger.info('Setting up hub environment')
        initial_setup = True
        subprocess.check_output(['apt-get', 'update', '--yes'], stderr=subprocess.STDOUT)
        subprocess.check_output(['apt-get', 'install', '--yes', 'python3', 'python3-venv'], stderr=subprocess.STDOUT)
        logger.info('Installed python & virtual environment')
        os.makedirs(hub_prefix, exist_ok=True)
        subprocess.check_output(['python3', '-m', 'venv', hub_prefix], stderr=subprocess.STDOUT)
        logger.info('Set up hub virtual environment')

    if initial_setup:
        logger.info('Setting up TLJH installer...')
    else:
        logger.info('Upgrading TLJH installer...')

    pip_flags = ['--upgrade']
    if os.environ.get('TLJH_BOOTSTRAP_DEV', 'no') == 'yes':
        pip_flags.append('--editable')
    tljh_repo_path = os.environ.get(
        'TLJH_BOOTSTRAP_PIP_SPEC',
        'git+https://github.com/jupyterhub/the-littlest-jupyterhub.git'
    )

    subprocess.check_output([
        os.path.join(hub_prefix, 'bin', 'pip'),
        'install'
    ] + pip_flags + [tljh_repo_path], stderr=subprocess.STDOUT)
    logger.info('Setup tljh package')

    logger.info('Starting TLJH installer...')
    os.execv(
        os.path.join(hub_prefix, 'bin', 'python3'),
        [
            os.path.join(hub_prefix, 'bin', 'python3'),
            '-m',
            'tljh.installer',
        ] + sys.argv[1:]
    )


if __name__ == '__main__':
    main()
