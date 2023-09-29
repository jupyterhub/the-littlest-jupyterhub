(topic-three-environments)=

# The system, hub, and user environments

TLJH's documentation mentions the _system environment_, the _hub environment_,
and the _user environment_. This section will introduce what is meant with that
and clarify the distinctions between the environments.

(system-environment)=

## The system environment

When this documentation mentions the _system environment_, it refers to the
Linux environment with its installed `apt` packages, users in `/etc/passwd`,
etc.

A part of the system environment is a Python environment setup via the `apt`
package `python` installed by default in Linux distributions supported by TLJH.
To be specific, we can refer to this as the _system's Python environment_.

If you would do `sudo python3 -m pip install <something>` you would end up
installing something in the system's Python environment, and that would not be
available in the hub environment or the user environment.

The system's Python environment is only used by TLJH to run the `bootstrap.py`
script downloaded as part of installing or upgrading TLJH. This script is also
responsible for setting up the hub environment.

(hub-environment)=

## The hub environment

The _hub environment_ is a [virtual Python environment] setup in `/opt/tljh/hub`
by the `bootstrap.py` script using the system's Python environment during TLJH
installation.

The hub environment has Python packages installed in it related to running
JupyterHub itself such as an JupyterHub authenticator package, but it doesn't
include packages to start user servers like JupyterLab.

When TLJH is installed/upgraded, the packages listed in
[tljh/requirements-hub-env.txt] are installed/upgraded in this environment.

If you would do `sudo /opt/tljh/hub/bin/python3 -m pip install <something>` you
would end up installing something in the hub environment, and that would not be
available in the system's Python environment or the user environment.

[virtual Python environment]: https://docs.python.org/3/library/venv.html

[tljh/requirements-hub-env.txt]: https://github.com/jupyterhub/the-littlest-jupyterhub/blob/HEAD/tljh/requirements-hub-env.txt

(user-environment)=

## The user environment

The _user environment_ is a Python environment setup in `/opt/tljh/user` by the
TLJH installer during TLJH installation. The user environment is not a virtual
environment because an entirely separate installation of Python has been made
for it.

The user environment has packages installed in it related to running individual
jupyter servers, such as `jupyterlab`.

When TLJH is _installed_, the packages listed in
[tljh/requirements-user-env.txt] are installed in this environment. When TLJH is
_upgraded_ though, as little as possible is done to this environment. Typically
only `jupyterhub` is upgraded to match the version in the hub environment. If
upgrading to a new major version of TLJH, then something small may be done
besides this, and then it should be described the changelog.

If you would do `sudo /opt/tljh/user/bin/python3 -m pip install <something>`, or
from a user server's terminal do `sudo -E pip install <something>` you would end
up installing something in the user environment, and that would not be available
in the system's Python environment or the hub environment.

[tljh/requirements-user-env-extras.txt]: https://github.com/jupyterhub/the-littlest-jupyterhub/blob/HEAD/tljh/requirements-user-env-extras.txt
