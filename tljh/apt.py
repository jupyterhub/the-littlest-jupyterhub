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
    # If gpg2 doesn't exist, install it.
    if not os.path.exists('/usr/bin/gpg2'):
        install_packages(['gnupg2'])
    subprocess.check_output(['apt-key', 'add', '-'], input=key, stderr=subprocess.STDOUT)


def add_source(name, source_url, section):
    """
    Add a debian package source.

    distro is determined from /etc/os-release
    """
    # lsb_release is not installed in most docker images by default
    distro = subprocess.check_output(['/bin/bash', '-c', 'source /etc/os-release && echo ${VERSION_CODENAME}'], stderr=subprocess.STDOUT).decode().strip()
    line = f'deb {source_url} {distro} {section}'
    with open(os.path.join('/etc/apt/sources.list.d/', name + '.list'), 'a+') as f:
        # Write out deb line only if it already doesn't exist
        if f.read() != line:
            f.seek(0)
            f.write(line)
            f.truncate()
            subprocess.check_output(['apt-get', 'update', '--yes'], stderr=subprocess.STDOUT)


def install_packages(packages):
    """
    Install debian packages
    """
    # Check if an apt-get update is required
    if len(os.listdir('/var/lib/apt/lists')) == 0:
        subprocess.check_output(['apt-get', 'update', '--yes'], stderr=subprocess.STDOUT)
    subprocess.check_output([
        'apt-get',
        'install',
        '--yes'
    ] + packages, stderr=subprocess.STDOUT)
