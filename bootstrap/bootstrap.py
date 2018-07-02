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
import urllib.request
import contextlib
import hashlib
import tempfile


def md5_file(fname):
    """
    Return md5 of a given filename

    Copied from https://stackoverflow.com/a/3431838
    """
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def check_miniconda_version(prefix, version):
    """
    Return true if a miniconda install with version exists at prefix
    """
    try:
        return subprocess.check_output([
            os.path.join(prefix, 'bin', 'conda'),
            '-V'
        ]).decode().strip() == 'conda {}'.format(version)
    except (subprocess.CalledProcessError, FileNotFoundError):
        # Conda doesn't exist, or wrong version
        return False


@contextlib.contextmanager
def download_miniconda_installer(version):
    md5sums = {
        '4.5.4': "a946ea1d0c4a642ddf0c3a26a18bb16d"
    }

    if version not in md5sums:
        raise ValueError(
            'minicondaversion {} not supported. Supported version:'.format(
                version, ' '.join(md5sums.keys())
            ))

    with tempfile.NamedTemporaryFile() as f:
        installer_url = "https://repo.continuum.io/miniconda/Miniconda3-{}-Linux-x86_64.sh".format(version)
        urllib.request.urlretrieve(installer_url, f.name)

        if md5_file(f.name) != md5sums[version]:
            raise Exception('md5 hash mismatch! Downloaded file corrupted')

        yield f.name


def install_miniconda(installer_path, prefix):
    subprocess.check_output([
        '/bin/bash',
        installer_path,
        '-u', '-b',
        '-p', prefix
    ], stderr=subprocess.STDOUT)


def pip_install(prefix, packages, editable=False):
    flags = '--no-cache-dir --upgrade'
    if editable:
        flags += '--editable'
    subprocess.check_output([
        os.path.join(prefix, 'bin', 'python3'),
        '-m', 'pip',
        'install', '--no-cache-dir',
    ] + packages)


def main():
    install_prefix = os.environ.get('TLJH_INSTALL_PREFIX', '/opt/tljh')
    hub_prefix = os.path.join(install_prefix, 'hub')
    miniconda_version = '4.5.4'

    print('Checking if TLJH is already installed...')
    if not check_miniconda_version(hub_prefix, miniconda_version):
        initial_setup = True
        print('Downloading & setting up hub environment...')
        with download_miniconda_installer(miniconda_version) as installer_path:
            install_miniconda(installer_path, hub_prefix)
        print('Hub environment set up!')
    else:
        initial_setup = False
        print('TLJH is already installed, will try to upgrade')

    if initial_setup:
        print('Setting up TLJH installer...')
    else:
        print('Upgrading TLJH installer...')

    pip_install(hub_prefix, [
        os.environ.get('TLJH_BOOTSTRAP_PIP_SPEC', 'git+https://github.com/yuvipanda/the-littlest-jupyterhub.git')
    ], editable=os.environ.get('TLJH_BOOTSTRAP_DEV', 'no') == 'yes')

    print('Starting TLJH installer...')
    os.execl(
        os.path.join(hub_prefix, 'bin', 'python3'),
        os.path.join(hub_prefix, 'bin', 'python3'),
        '-m',
        'tljh.installer'
    )

if __name__ == '__main__':
    main()
