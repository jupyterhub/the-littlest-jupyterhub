"""
Utilities for working with the apt package manager
"""
import os
import subprocess


def trust_gpg_key(key):
    """
    Trust given GPG public key.

    key is a GPG public key (bytes) that can be passed to apt-key add via stdin.
    """
    subprocess.run(['apt-key', 'add', '-'], input=key, check=True)


def add_source(name, source_url, section):
    """
    Add a debian package source.

    distro is determined from /etc/os-release
    """
    # lsb_release is not installed in most docker images by default
    distro = subprocess.check_output(['/bin/bash', '-c', 'source /etc/os-release && echo ${VERSION_CODENAME}']).decode().strip()
    line = f'deb {source_url} {distro} {section}'
    with open(os.path.join('/etc/apt/sources.list.d/', name + '.list'), 'a+') as f:
        # Write out deb line only if it already doesn't exist
        if f.read() != line:
            f.seek(0)
            f.write(line)
            f.truncate()
            subprocess.check_output(['apt-get', 'update', '--yes'])


def install_packages(packages):
    """
    Install debian packages
    """
    subprocess.check_output([
        'apt-get',
        'install',
        '--yes'
    ] + packages)
