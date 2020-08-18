"""
Test running bootstrap script in different circumstances
"""
import concurrent.futures
import requests
import subprocess
from textwrap import dedent
import time

def run_bootstrap(container_name, image, flags=None):
    # stop container if it is already running
    subprocess.run([
        'docker', 'rm', '-f', container_name
    ])
    
    # Start a detached Ubuntu 16.04 container
    subprocess.check_call([
        'docker', 'run', '--detach', '--publish', '12000:80', '--name', container_name, image,
        '/bin/bash', '-c', 'sleep 1000s'
    ])
    # Install python3 inside the ubuntu container
    # There is no trusted Ubuntu+Python3 container we can use
    subprocess.check_output([
        'docker', 'exec', container_name, 'apt-get', 'update'
    ])

    if flags:
        pkgs = ['python3', 'systemd', 'git']
    else:
        pkgs = ['python3']
    subprocess.check_output([
        'docker', 'exec', container_name, 'apt-get', 'install', '--yes'] + pkgs
    )
    # Copy only the bootstrap script  to container, so this is faster
    subprocess.check_call([
        'docker',
        'cp',
        'bootstrap/', f'{container_name}:/srv'
    ])

    # Run bootstrap script, return the output
    return subprocess.run([
        'docker', 'exec', '-i', container_name,
        'python3', '/srv/bootstrap/bootstrap.py'
    ] + flags, check=False, stdout=subprocess.PIPE, encoding='utf-8')

def test_ubuntu_too_old():
    """
    Error with a useful message when running in older Ubuntu
    """
    output = run_bootstrap('old-distro-test', 'ubuntu:16.04')
    assert output.stdout == 'The Littlest JupyterHub requires Ubuntu 18.04 or higher\n'
    assert output.returncode == 1


def test_inside_no_systemd_docker():
    output = run_bootstrap('plain-docker-test', 'ubuntu:18.04')
    assert output.stdout.strip() == dedent("""
        Systemd is required to run TLJH
        Running inside a docker container without systemd isn't supported
        We recommend against running a production TLJH instance inside a docker container
        For local development, see http://tljh.jupyter.org/en/latest/contributing/dev-setup.html
    """).strip()
    assert output.returncode == 1


def verify_progress_page(expected_status_code, timeout):
    progress_page_status = False
    start = time.time()
    print("in verify_progress_page")
    while not progress_page_status and (time.time() - start < timeout):
        try:
            resp = requests.get('http://127.0.0.1:12000/index.html')
            if resp.status_code == expected_status_code:
                progress_page_status = True
                break;
        except Exception as e:
            time.sleep(2)
            continue;

    return progress_page_status

def test_progress_page():
    with concurrent.futures.ThreadPoolExecutor() as executor:
        installer = executor.submit(run_bootstrap, 'progress-page', 'ubuntu:18.04', ['--show-progress-page'])
        print("started installer")

        # Check if progress page started
        started = verify_progress_page(expected_status_code=200, timeout=120)
        print("started")
        assert started

        return_value = installer.result()
        print("return value")

        # Check if progress page stopped
        stopped = verify_progress_page(expected_status_code=404, timeout=120)
        assert stopped
