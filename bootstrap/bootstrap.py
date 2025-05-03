"""
Bootstrap an installation of TLJH.

Sets up just enough TLJH environments to invoke tljh.installer.

This script is run as:

    curl <script-url> | sudo python3 -

Constraints:

    - The entire script should be compatible with Python 3.9, which is the default on
      Debian 11.
    - The script should parse in Python 3.8 as we print error messages for using
      Ubuntu 20.04 which comes with Python 3.8 by default.
    - The script must depend only on stdlib modules, as no previous installation
      of dependencies can be assumed.

Environment variables:

    TLJH_INSTALL_PREFIX         Defaults to "/opt/tljh", determines the location
                                of the tljh installations root folder.
    TLJH_BOOTSTRAP_PIP_SPEC     From this location, the bootstrap script will
                                pip install --upgrade the tljh installer.
    TLJH_BOOTSTRAP_DEV          Determines if --editable is passed when
                                installing the tljh installer. Pass the values
                                yes or no.

Command line flags, from "bootstrap.py --help":

    The bootstrap.py script accept the following command line flags. All other
    flags are passed through to the tljh installer without interception by this
    script.

    --show-progress-page    Starts a local web server listening on port 80 where
                            logs can be accessed during installation. If this is
                            passed, it will pass --progress-page-server-pid=<pid>
                            to the tljh installer for later termination.
    --version VERSION       TLJH version or Git reference. Default 'latest' is
                            the most recent release. Partial versions can be
                            specified, for example '1', '1.0' or '1.0.0'. You
                            can also pass a branch name such as 'main' or a
                            commit hash.
"""

import logging
import multiprocessing
import os
import re
import shutil
import subprocess
import sys
import urllib.request
from argparse import ArgumentParser
from http.server import HTTPServer, SimpleHTTPRequestHandler

progress_page_favicon_url = "https://raw.githubusercontent.com/jupyterhub/jupyterhub/main/share/jupyterhub/static/favicon.ico"
progress_page_html = """
<html>
<head>
  <title>The Littlest Jupyterhub</title>
</head>
<body>
  <meta http-equiv="refresh" content="30" >
  <meta http-equiv="content-type" content="text/html; charset=utf-8">
  <meta name="viewport" content="width=device-width">
  <img class="logo" src="https://raw.githubusercontent.com/jupyterhub/the-littlest-jupyterhub/HEAD/docs/_static/images/logo/logo.png">
  <div class="loader center"></div>
  <div class="center main-msg">Please wait while your TLJH is setting up...</div>
  <div class="center logs-msg">Click the button below to see the logs</div>
  <div class="center tip" >Tip: to update the logs, refresh the page</div>
  <button class="logs-button center" onclick="window.location.href='/logs'">View logs</button>
</body>

  <style>
    button:hover {
      background: grey;
    }

    .logo {
      width: 150px;
      height: auto;
    }
    .center {
      margin: 0 auto;
      margin-top: 50px;
      text-align:center;
      display: block;
    }
    .main-msg {
      font-size: 30px;
      font-weight: bold;
      color: grey;
      text-align:center;
    }
    .logs-msg {
      font-size: 15px;
      color: grey;
    }
    .tip {
      font-size: 13px;
      color: grey;
      margin-top: 10px;
      font-style: italic;
    }
    .logs-button {
      margin-top:15px;
      border: 0;
      color: white;
      padding: 15px 32px;
      font-size: 16px;
      cursor: pointer;
      background: #f5a252;
    }
    .loader {
      width: 150px;
      height: 150px;
      border-radius: 90%;
      border: 7px solid transparent;
      animation: spin 2s infinite ease;
      animation-direction: alternate;
    }
    @keyframes spin {
      0% {
        transform: rotateZ(0deg);
        border-top-color: #f17c0e
      }
      100% {
        transform: rotateZ(360deg);
        border-top-color: #fce5cf;
      }
    }
  </style>
</head>
</html>
"""

logger = logging.getLogger(__name__)


def _parse_version(vs):
    """Parse a simple version into a tuple of ints"""
    return tuple(int(part) for part in vs.split("."))


# This function is needed both by the process starting this script, and by the
# TLJH installer that this script execs in the end. Make sure its replica at
# tljh/utils.py stays in sync with this version!
def run_subprocess(cmd, *args, **kwargs):
    """
    Run given cmd with smart output behavior.

    If command succeeds, print output to debug logging.
    If it fails, print output to info logging.

    In TLJH, this sends successful output to the installer log,
    and failed output directly to the user's screen
    """
    logger = logging.getLogger("tljh")
    proc = subprocess.run(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, *args, **kwargs
    )
    printable_command = " ".join(cmd)
    if proc.returncode != 0:
        # Our process failed! Show output to the user
        logger.error(
            "Ran {command} with exit code {code}".format(
                command=printable_command, code=proc.returncode
            )
        )
        logger.error(proc.stdout.decode())
        raise subprocess.CalledProcessError(cmd=cmd, returncode=proc.returncode)
    else:
        # This goes into installer.log
        logger.debug(
            "Ran {command} with exit code {code}".format(
                command=printable_command, code=proc.returncode
            )
        )
        output = proc.stdout.decode()
        # This produces multi line log output, unfortunately. Not sure how to fix.
        # For now, prioritizing human readability over machine readability.
        logger.debug(output)
        return output


def get_os_release_variable(key):
    """
    Return value for key from /etc/os-release

    /etc/os-release is a bash file, so should use bash to parse it.

    Returns empty string if key is not found.
    """
    return (
        subprocess.check_output(
            [
                "/bin/bash",
                "-c",
                "source /etc/os-release && echo ${{{key}}}".format(key=key),
            ]
        )
        .decode()
        .strip()
    )

def host_has_systemd() -> bool:
    if shutil.which("systemd"):
        return True
    if shutil.which("systemctl"):
        return True
    return False

def ensure_host_system_can_install_tljh():
    """
    Check if TLJH is installable in current host system and exit with a clear
    error message otherwise.
    """
    # Require Ubuntu 22.04+ or Debian 11+
    distro = get_os_release_variable("ID")
    version = get_os_release_variable("VERSION_ID")
    if distro not in ["ubuntu", "debian"]:
        print("The Littlest JupyterHub currently supports Ubuntu or Debian Linux only")
        sys.exit(1)
    elif distro == "ubuntu" and _parse_version(version) < (22, 4):
        print("The Littlest JupyterHub requires Ubuntu 22.04 or higher")
        sys.exit(1)
    elif distro == "debian" and _parse_version(version) < (11,):
        print("The Littlest JupyterHub requires Debian 11 or higher")
        sys.exit(1)

    # Require Python 3.9+
    if sys.version_info < (3, 9):
        print(f"bootstrap.py must be run with at least Python 3.9, found {sys.version}")
        sys.exit(1)

    # Require systemd (systemctl is a part of systemd)
    if not any([shutil.which("systemctl"), shutil.which("systemd")]):
        print("Systemd is required to run TLJH")
        # Provide additional information about running in docker containers
        if os.path.exists("/.dockerenv"):
            print("Running inside a docker container without systemd isn't supported")
            print(
                "We recommend against running a production TLJH instance inside a docker container"
            )
            print(
                "For local development, see http://tljh.jupyter.org/en/latest/contributing/dev-setup.html"
            )
        sys.exit(1)
    return distro, version


class ProgressPageRequestHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/logs":
            with open("/opt/tljh/installer.log") as log_file:
                logs = log_file.read()

            self.send_response(200)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.end_headers()
            self.wfile.write(logs.encode("utf-8"))
        elif self.path == "/index.html":
            self.path = "/var/run/index.html"
            return SimpleHTTPRequestHandler.do_GET(self)
        elif self.path == "/favicon.ico":
            self.path = "/var/run/favicon.ico"
            return SimpleHTTPRequestHandler.do_GET(self)
        elif self.path == "/":
            self.send_response(302)
            self.send_header("Location", "/index.html")
            self.end_headers()
        else:
            SimpleHTTPRequestHandler.send_error(self, code=403)


def _find_matching_version(all_versions, requested):
    """
    Find the latest version that is less than or equal to requested.
    all_versions must be int-tuples.
    requested must be an int-tuple or "latest"

    Returns None if no version is found.
    """
    sorted_versions = sorted(all_versions, reverse=True)
    if requested == "latest":
        return sorted_versions[0]
    components = len(requested)
    for v in sorted_versions:
        if v[:components] == requested:
            return v
    return None


def _resolve_git_version(version):
    """
    Resolve the version argument to a git ref using git ls-remote
    - If version looks like MAJOR.MINOR.PATCH or a partial tag then fetch all tags
      and return the most latest tag matching MAJOR.MINOR.PATCH
      (e.g. version=0.1 -> 0.1.PATCH). This should ignore dev tags
    - If version='latest' then return the latest release tag
    - Otherwise assume version is a branch or hash and return it without checking
    """

    if version != "latest" and not re.match(r"\d+(\.\d+)?(\.\d+)?$", version):
        return version

    all_versions = set()
    out = run_subprocess(
        [
            "git",
            "ls-remote",
            "--tags",
            "--refs",
            "https://github.com/jupyterhub/the-littlest-jupyterhub.git",
        ]
    )

    for line in out.splitlines():
        m = re.match(r"(?P<sha>[a-f0-9]+)\s+refs/tags/(?P<tag>[\S]+)$", line)
        if not m:
            raise Exception("Unexpected git ls-remote output: {}".format(line))
        tag = m.group("tag")
        if tag == version:
            return tag
        if re.match(r"\d+\.\d+\.\d+$", tag):
            all_versions.add(tuple(int(v) for v in tag.split(".")))

    if not all_versions:
        raise Exception("No MAJOR.MINOR.PATCH git tags found")

    if version == "latest":
        requested = "latest"
    else:
        requested = tuple(int(v) for v in version.split("."))
    found = _find_matching_version(all_versions, requested)
    if not found:
        raise Exception(
            "No version matching {} found {}".format(version, sorted(all_versions))
        )
    return ".".join(str(f) for f in found)


def main():
    """
    This bootstrap script intercepts some command line flags, everything else is
    passed through to the TLJH installer script.

    The --show-progress-page flag indicates that the bootstrap script should
    start a local webserver temporarily and report its installation progress via
    a web site served locally on port 80.
    """
    distro, version = ensure_host_system_can_install_tljh()

    parser = ArgumentParser(
        description=(
            "The bootstrap.py script accept the following command line flags. "
            "All other flags are passed through to the tljh installer without "
            "interception by this script."
        )
    )
    parser.add_argument(
        "--show-progress-page",
        action="store_true",
        help=(
            "Starts a local web server listening on port 80 where logs can be "
            "accessed during installation. If this is passed, it will pass "
            "--progress-page-server-pid=<pid> to the tljh installer for later "
            "termination."
        ),
    )
    parser.add_argument(
        "--version",
        default="",
        help=(
            "TLJH version or Git reference. "
            "Default 'latest' is the most recent release. "
            "Partial versions can be specified, for example '1', '1.0' or '1.0.0'. "
            "You can also pass a branch name such as 'main' or a commit hash."
        ),
    )
    args, tljh_installer_flags = parser.parse_known_args()

    # Various related constants
    install_prefix = os.environ.get("TLJH_INSTALL_PREFIX", "/opt/tljh")
    hub_env_prefix = os.path.join(install_prefix, "hub")
    hub_env_python = os.path.join(hub_env_prefix, "bin", "python3")
    hub_env_pip = os.path.join(hub_env_prefix, "bin", "pip")
    initial_setup = not os.path.exists(hub_env_python)

    # Attempt to start a web server to serve a progress page reporting
    # installation progress.
    if args.show_progress_page:
        # Write HTML and a favicon to be served by our webserver
        with open("/var/run/index.html", "w+") as f:
            f.write(progress_page_html)
        urllib.request.urlretrieve(progress_page_favicon_url, "/var/run/favicon.ico")

        # If TLJH is already installed and Traefik is already running, port 80
        # will be busy and we will get an "Address already in use" error. This
        # is acceptable and we can ignore the error.
        try:
            # Serve the loading page until manually aborted or until the TLJH
            # installer terminates the process
            def serve_forever(server):
                try:
                    server.serve_forever()
                except KeyboardInterrupt:
                    pass

            progress_page_server = HTTPServer(("", 80), ProgressPageRequestHandler)
            p = multiprocessing.Process(
                target=serve_forever, args=(progress_page_server,)
            )
            p.start()

            # Pass the server's pid to the installer for later termination
            tljh_installer_flags.extend(["--progress-page-server-pid", str(p.pid)])
        except OSError:
            pass

    # Set up logging to print to a file and to stderr
    os.makedirs(install_prefix, exist_ok=True)
    file_logger_path = os.path.join(install_prefix, "installer.log")
    file_logger = logging.FileHandler(file_logger_path)
    # installer.log should be readable only by root
    os.chmod(file_logger_path, 0o500)

    file_logger.setFormatter(logging.Formatter("%(asctime)s %(message)s"))
    file_logger.setLevel(logging.DEBUG)
    logger.addHandler(file_logger)

    stderr_logger = logging.StreamHandler()
    stderr_logger.setFormatter(logging.Formatter("%(message)s"))
    stderr_logger.setLevel(logging.INFO)
    logger.addHandler(stderr_logger)

    logger.setLevel(logging.DEBUG)

    if not initial_setup:
        logger.info("Existing TLJH installation detected, upgrading...")
    else:
        logger.info("Existing TLJH installation not detected, installing...")
        logger.info("Setting up hub environment...")
        logger.info("Installing Python, venv, pip, and git via apt-get...")

        # In some very minimal base VM images, it looks like the "universe" apt
        # package repository is disabled by default, causing bootstrapping to
        # fail. We install the software-properties-common package so we can get
        # the add-apt-repository command to make sure the universe repository is
        # enabled, since that's where the python3-pip package lives.
        #
        # In Ubuntu 21.10 DEBIAN_FRONTEND has found to be needed to avoid
        # getting stuck on an input prompt during apt-get install.
        #
        apt_get_adjusted_env = os.environ.copy()
        apt_get_adjusted_env["DEBIAN_FRONTEND"] = "noninteractive"
        run_subprocess(["apt-get", "update"])
        run_subprocess(
            ["apt-get", "install", "--yes", "software-properties-common"],
            env=apt_get_adjusted_env,
        )
        # Section "universe" exists and is required only in ubuntu.
        if distro == "ubuntu":
            run_subprocess(["add-apt-repository", "universe", "--yes"])
        run_subprocess(["apt-get", "update"])
        run_subprocess(
            [
                "apt-get",
                "install",
                "--yes",
                "python3",
                "python3-venv",
                "python3-pip",
                "git",
                "sudo",  # sudo is missing in default debian install
            ],
            env=apt_get_adjusted_env,
        )

        logger.info("Setting up virtual environment at {}".format(hub_env_prefix))
        os.makedirs(hub_env_prefix, exist_ok=True)
        run_subprocess(["python3", "-m", "venv", hub_env_prefix])

    logger.info("Upgrading pip...")
    run_subprocess([hub_env_pip, "install", "--upgrade", "pip"])

    # pip install TLJH installer based on
    #
    #   1. --version, _resolve_git_version is used
    #   2. TLJH_BOOTSTRAP_PIP_SPEC (then also respect TLJH_BOOTSTRAP_DEV)
    #   3. latest, _resolve_git_version is used
    #
    tljh_install_cmd = [hub_env_pip, "install", "--upgrade"]
    bootstrap_pip_spec = os.environ.get("TLJH_BOOTSTRAP_PIP_SPEC")
    if args.version or not bootstrap_pip_spec:
        version_to_resolve = args.version or "latest"
        bootstrap_pip_spec = (
            "git+https://github.com/jupyterhub/the-littlest-jupyterhub.git@{}".format(
                _resolve_git_version(version_to_resolve)
            )
        )
    elif os.environ.get("TLJH_BOOTSTRAP_DEV", "no") == "yes":
        logger.info("Selected TLJH_BOOTSTRAP_DEV=yes...")
        tljh_install_cmd.append("--editable")
    tljh_install_cmd.append(bootstrap_pip_spec)

    if initial_setup:
        logger.info("Installing TLJH installer...")
    else:
        logger.info("Upgrading TLJH installer...")
    run_subprocess(tljh_install_cmd)

    # Run TLJH installer
    logger.info("Running TLJH installer...")
    os.execv(
        hub_env_python, [hub_env_python, "-m", "tljh.installer"] + tljh_installer_flags
    )


if __name__ == "__main__":
    main()
