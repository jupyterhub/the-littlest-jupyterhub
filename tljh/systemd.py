"""
Wraps systemctl to install, uninstall, start & stop systemd services.

We use sudo + subprocess calls for everything. This works when we
are running as root & as normal user (with arbitrary sudo privileges).
Arbitrary sudo privileges suck, but are better than running the whole
process as root.

If we use a debian package instead, we can get rid of all this code.
"""
import subprocess
import os


def reload_daemon():
    """
    Equivalent to systemctl daemon-reload.

    Makes systemd discover new units.
    """
    subprocess.run([
        'sudo',
        'systemctl',
        'daemon-reload'
    ], check=True)


def install_unit(name, unit, path='/etc/systemd/system'):
    """
    Install unit wih given name
    """
    subprocess.run([
        'sudo',
        'tee',
        os.path.join(path, name)
    ], input=unit.encode('utf-8'), check=True)


def uninstall_unit(name, path='/etc/systemd/system'):
    """
    Uninstall unit with given name
    """
    subprocess.run([
        'sudo',
        'rm',
        os.path.join(path, name)
    ], check=True)


def start_service(name):
    """
    Start service with given name.
    """
    subprocess.run([
        'sudo',
        'systemctl',
        'start',
        name
    ], check=True)
