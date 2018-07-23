"""
Bootstrap an installation of TLJH.

Sets up just enough TLJH environments to invoke tljh.installer.

This script is run as:

    curl <script-url> | sudo python3 -

Constraints:
  - Be compatible with Python 3.4 (since we support Ubuntu 16.04)
  - Use stdlib modules only
"""
import os
import subprocess
import sys


def main():
    install_prefix = os.environ.get('TLJH_INSTALL_PREFIX', '/opt/tljh')
    hub_prefix = os.path.join(install_prefix, 'hub')

    print('Checking if TLJH is already installed...')
    if os.path.exists(os.path.join(hub_prefix, 'bin', 'python3')):
        print('TLJH already installed, upgrading...')
        initial_setup = False
    else:
        print('Setting up hub environment')
        initial_setup = True
        subprocess.check_output(['apt-get', 'update', '--yes'])
        subprocess.check_output(['apt-get', 'install', '--yes', 'python3', 'python3-venv'])
        os.makedirs(hub_prefix, exist_ok=True)
        subprocess.check_output(['python3', '-m', 'venv', hub_prefix])

    if initial_setup:
        print('Setting up TLJH installer...')
    else:
        print('Upgrading TLJH installer...')

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
    ] + pip_flags + [tljh_repo_path])

    print('Starting TLJH installer...')
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
