"""
Wraps systemctl to install, uninstall, start & stop systemd services.

If we use a debian package instead, we can get rid of all this code.
"""
import subprocess
import os


def reload_daemon():
    """
    Equivalent to systemctl daemon-reload.

    Makes systemd discover new units.
    """
    subprocess.run(["systemctl", "daemon-reload"], check=True)


def install_unit(name, unit, path="/etc/systemd/system"):
    """
    Install unit with given name
    """
    with open(os.path.join(path, name), "w") as f:
        f.write(unit)


def uninstall_unit(name, path="/etc/systemd/system"):
    """
    Uninstall unit with given name
    """
    subprocess.run(["rm", os.path.join(path, name)], check=True)


def start_service(name):
    """
    Start service with given name.
    """
    subprocess.run(["systemctl", "start", name], check=True)


def stop_service(name):
    """
    Start service with given name.
    """
    subprocess.run(["systemctl", "stop", name], check=True)


def restart_service(name):
    """
    Restart service with given name.
    """
    subprocess.run(["systemctl", "restart", name], check=True)


def enable_service(name):
    """
    Enable a service with given name.

    This most likely makes the service start on bootup
    """
    subprocess.run(["systemctl", "enable", name], check=True)


def disable_service(name):
    """
    Enable a service with given name.

    This most likely makes the service start on bootup
    """
    subprocess.run(["systemctl", "disable", name], check=True)


def check_service_active(name):
    """
    Check if a service is currently active (running)
    """
    try:
        subprocess.run(["systemctl", "is-active", name], check=True)
        return True
    except subprocess.CalledProcessError:
        return False


def check_service_enabled(name):
    """
    Check if a service is enabled
    """
    try:
        subprocess.run(["systemctl", "is-enabled", name], check=True)
        return True
    except subprocess.CalledProcessError:
        return False
