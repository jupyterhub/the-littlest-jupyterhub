"""
Bootstrap an installation of TLJH.

Sets up just enough TLJH environments to invoke tljh.installer.

This script is run as:

    curl <script-url> | sudo python3 -

Constraints:

    - The entire script should be compatible with Python 3.6, which is the on
      Ubuntu 18.04+.
    - The script should parse in Python 3.5 as we print error messages for using
      Ubuntu 16.04+ which comes with Python 3.5 by default. This means no
      f-strings can be used.
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

Command line flags:

    The bootstrap.py script accept the following command line flags. All other
    flags are passed through to the tljh installer without interception by this
    script.

    --show-progress-page    Starts a local web server listening on port 80 where
                            logs can be accessed during installation. If this is
                            passed, it will pass --progress-page-server-pid=<pid>
                            to the tljh installer for later termination.
"""
import os
from http.server import SimpleHTTPRequestHandler, HTTPServer
import multiprocessing
import subprocess
import sys
import logging
import shutil
import urllib.request

progress_page_favicon_url = "https://raw.githubusercontent.com/jupyterhub/jupyterhub/HEAD/share/jupyterhub/static/favicon.ico"
progress_page_html = """
<html>
<head>
  <title>The Littlest Jupyterhub</title>
</head>
<body>
  <meta http-equiv="refresh" content="30" >
  <meta http-equiv="content-type" content="text/html; charset=utf-8">
  <meta name="viewport" content="width=device-width">
  <img class="logo" src="https://raw.githubusercontent.com/jupyterhub/the-littlest-jupyterhub/HEAD/docs/images/logo/logo.png">
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
        # This produces multi line log output, unfortunately. Not sure how to fix.
        # For now, prioritizing human readability over machine readability.
        logger.debug(proc.stdout.decode())


def ensure_host_system_can_install_tljh():
    """
    Check if TLJH is installable in current host system and exit with a clear
    error message otherwise.
    """

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

    # Require Ubuntu 18.04+
    distro = get_os_release_variable("ID")
    version = float(get_os_release_variable("VERSION_ID"))
    if distro != "ubuntu":
        print("The Littlest JupyterHub currently supports Ubuntu Linux only")
        sys.exit(1)
    elif float(version) < 18.04:
        print("The Littlest JupyterHub requires Ubuntu 18.04 or higher")
        sys.exit(1)

    # Require Python 3.6+
    if sys.version_info < (3, 6):
        print("bootstrap.py must be run with at least Python 3.6")
        sys.exit(1)

    # Require systemd (systemctl is a part of systemd)
    if not shutil.which("systemd") or not shutil.which("systemctl"):
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


def main():
    """
    This script intercepts the --show-progress-page flag, but all other flags
    are passed through to the TLJH installer script.

    The --show-progress-page flag indicates that the bootstrap script should
    start a local webserver temporarily and report its installation progress via
    a web site served locally on port 80.
    """
    ensure_host_system_can_install_tljh()

    # Various related constants
    install_prefix = os.environ.get("TLJH_INSTALL_PREFIX", "/opt/tljh")
    hub_prefix = os.path.join(install_prefix, "hub")
    python_bin = os.path.join(hub_prefix, "bin", "python3")
    pip_bin = os.path.join(hub_prefix, "bin", "pip")
    initial_setup = not os.path.exists(python_bin)

    # Attempt to start a web server to serve a progress page reporting
    # installation progress.
    tljh_installer_flags = sys.argv[1:]
    if "--show-progress-page" in tljh_installer_flags:
        # Remove the bootstrap specific flag and let all other flags pass
        # through to the installer.
        tljh_installer_flags.remove("--show-progress-page")

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
            ],
            env=apt_get_adjusted_env,
        )

        logger.info("Setting up virtual environment at {}".format(hub_prefix))
        os.makedirs(hub_prefix, exist_ok=True)
        run_subprocess(["python3", "-m", "venv", hub_prefix])

    # Upgrade pip
    # Keep pip version pinning in sync with the one in unit-test.yml!
    # See changelog at https://pip.pypa.io/en/latest/news/#changelog
    logger.info("Upgrading pip...")
    run_subprocess([pip_bin, "install", "--upgrade", "pip==21.3.*"])

    # Install/upgrade TLJH installer
    tljh_install_cmd = [pip_bin, "install", "--upgrade"]
    if os.environ.get("TLJH_BOOTSTRAP_DEV", "no") == "yes":
        tljh_install_cmd.append("--editable")
    tljh_install_cmd.append(
        os.environ.get(
            "TLJH_BOOTSTRAP_PIP_SPEC",
            "git+https://github.com/jupyterhub/the-littlest-jupyterhub.git",
        )
    )
    if initial_setup:
        logger.info("Installing TLJH installer...")
    else:
        logger.info("Upgrading TLJH installer...")
    run_subprocess(tljh_install_cmd)

    # Run TLJH installer
    logger.info("Running TLJH installer...")
    os.execv(python_bin, [python_bin, "-m", "tljh.installer"] + tljh_installer_flags)


if __name__ == "__main__":
    main()
