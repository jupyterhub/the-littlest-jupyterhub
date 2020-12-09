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
from http.server import SimpleHTTPRequestHandler, HTTPServer
import multiprocessing
import subprocess
import sys
import logging
import shutil
import urllib.request

html = """
<html>
<head>
    <title>The Littlest Jupyterhub</title>
</head>
<body>
  <meta http-equiv="refresh" content="30" >
  <meta http-equiv="content-type" content="text/html; charset=utf-8">
  <meta name="viewport" content="width=device-width">
  <img class="logo" src="https://raw.githubusercontent.com/jupyterhub/the-littlest-jupyterhub/master/docs/images/logo/logo.png">
  <div class="loader center"></div>
  <div class="center main-msg">Please wait while your TLJH is building...</div>
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

# Copied into tljh/utils.py. Make sure the copies are exactly the same!
def run_subprocess(cmd, *args, **kwargs):
    """
    Run given cmd with smart output behavior.

    If command succeeds, print output to debug logging.
    If it fails, print output to info logging.

    In TLJH, this sends successful output to the installer log,
    and failed output directly to the user's screen
    """
    logger = logging.getLogger('tljh')
    proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, *args, **kwargs)
    printable_command = ' '.join(cmd)
    if proc.returncode != 0:
        # Our process failed! Show output to the user
        logger.error('Ran {command} with exit code {code}'.format(
            command=printable_command, code=proc.returncode
        ))
        logger.error(proc.stdout.decode())
        raise subprocess.CalledProcessError(cmd=cmd, returncode=proc.returncode)
    else:
        # This goes into installer.log
        logger.debug('Ran {command} with exit code {code}'.format(
            command=printable_command, code=proc.returncode
        ))
        # This produces multi line log output, unfortunately. Not sure how to fix.
        # For now, prioritizing human readability over machine readability.
        logger.debug(proc.stdout.decode())

def validate_host():
    """
    Make sure TLJH is installable in current host
    """
    # Support only Ubuntu 18.04+
    distro = get_os_release_variable('ID')
    version = float(get_os_release_variable('VERSION_ID'))
    if distro != 'ubuntu':
        print('The Littlest JupyterHub currently supports Ubuntu Linux only')
        sys.exit(1)
    elif float(version) < 18.04:
        print('The Littlest JupyterHub requires Ubuntu 18.04 or higher')
        sys.exit(1)

    if sys.version_info < (3, 5):
        print("bootstrap.py must be run with at least Python 3.5")
        sys.exit(1)

    if not (shutil.which('systemd') and shutil.which('systemctl')):
        print("Systemd is required to run TLJH")
        # Only fail running inside docker if systemd isn't present
        if os.path.exists('/.dockerenv'):
            print("Running inside a docker container without systemd isn't supported")
            print("We recommend against running a production TLJH instance inside a docker container")
            print("For local development, see http://tljh.jupyter.org/en/latest/contributing/dev-setup.html")
        sys.exit(1)

class LoaderPageRequestHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/logs":
            with open("/opt/tljh/installer.log", "r") as log_file:
                logs = log_file.read()

            self.send_response(200)
            self.send_header('Content-Type', 'text/plain; charset=utf-8')
            self.end_headers()
            self.wfile.write(logs.encode('utf-8'))
        elif self.path == "/index.html":
            self.path = "/var/run/index.html"
            return SimpleHTTPRequestHandler.do_GET(self)
        elif self.path == "/favicon.ico":
            self.path = "/var/run/favicon.ico"
            return SimpleHTTPRequestHandler.do_GET(self)
        elif self.path == "/":
            self.send_response(302)
            self.send_header('Location','/index.html')
            self.end_headers()
        else:
            SimpleHTTPRequestHandler.send_error(self, code=403)

def serve_forever(server):
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass

def main():
    flags = sys.argv[1:]
    temp_page_flag = "--show-progress-page"

    # Check for flag in the argv list. This doesn't use argparse
    # because it's the only argument that's meant for the boostrap script.
    # All the other flags will be passed to and parsed by the installer.
    if temp_page_flag in flags:
        with open("/var/run/index.html", "w+") as f:
            f.write(html)
        favicon_url="https://raw.githubusercontent.com/jupyterhub/jupyterhub/master/share/jupyterhub/static/favicon.ico"
        urllib.request.urlretrieve(favicon_url, "/var/run/favicon.ico")

        # If the bootstrap is run to upgrade TLJH, then this will raise an "Address already in use" error
        try:
            loading_page_server = HTTPServer(("", 80), LoaderPageRequestHandler)
            p = multiprocessing.Process(target=serve_forever, args=(loading_page_server,))
            # Serves the loading page until TLJH builds
            p.start()

            # Remove the flag from the args list, since it was only relevant to this script.
            flags.remove("--show-progress-page")

            # Pass the server's pid as a flag to the istaller
            pid_flag = "--progress-page-server-pid"
            flags.extend([pid_flag, str(p.pid)])
        except OSError:
            # Only serve the loading page when installing TLJH
            pass

    validate_host()
    install_prefix = os.environ.get('TLJH_INSTALL_PREFIX', '/opt/tljh')
    hub_prefix = os.path.join(install_prefix, 'hub')

    # Set up logging to print to a file and to stderr
    os.makedirs(install_prefix, exist_ok=True)
    file_logger_path = os.path.join(install_prefix, 'installer.log')
    file_logger = logging.FileHandler(file_logger_path)
    # installer.log should be readable only by root
    os.chmod(file_logger_path, 0o500)

    file_logger.setFormatter(logging.Formatter('%(asctime)s %(message)s'))
    file_logger.setLevel(logging.DEBUG)
    logger.addHandler(file_logger)

    stderr_logger = logging.StreamHandler()
    stderr_logger.setFormatter(logging.Formatter('%(message)s'))
    stderr_logger.setLevel(logging.INFO)
    logger.addHandler(stderr_logger)
    logger.setLevel(logging.DEBUG)

    logger.info('Checking if TLJH is already installed...')
    if os.path.exists(os.path.join(hub_prefix, 'bin', 'python3')):
        logger.info('TLJH already installed, upgrading...')
        initial_setup = False
    else:
        logger.info('Setting up hub environment')
        initial_setup = True
        # Install software-properties-common, so we can get add-apt-repository
        # That helps us make sure the universe repository is enabled, since
        # that's where the python3-pip package lives. In some very minimal base
        # VM images, it looks like the universe repository is disabled by default,
        # causing bootstrapping to fail.
        run_subprocess(['apt-get', 'update', '--yes'])
        run_subprocess(['apt-get', 'install', '--yes', 'software-properties-common'])
        run_subprocess(['add-apt-repository', 'universe'])

        run_subprocess(['apt-get', 'update', '--yes'])
        run_subprocess(['apt-get', 'install', '--yes',
            'python3',
            'python3-venv',
            'python3-pip',
            'git'
        ])
        logger.info('Installed python & virtual environment')
        os.makedirs(hub_prefix, exist_ok=True)
        run_subprocess(['python3', '-m', 'venv', hub_prefix])
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
        'git+https://github.com/AVADOLearning/the-littlest-jupyterhub.git'
    )

    # Upgrade pip
    run_subprocess([
        os.path.join(hub_prefix, 'bin', 'pip'),
        'install',
        '--upgrade',
        'pip==20.0.*'
    ])
    logger.info('Upgraded pip')

    run_subprocess([
        os.path.join(hub_prefix, 'bin', 'pip'),
        'install'
    ] + pip_flags + [tljh_repo_path])
    logger.info('Setup tljh package')

    logger.info('Starting TLJH installer...')
    os.execv(
        os.path.join(hub_prefix, 'bin', 'python3'),
        [
            os.path.join(hub_prefix, 'bin', 'python3'),
            '-m',
            'tljh.installer',
        ] + flags
    )

if __name__ == '__main__':
    main()
