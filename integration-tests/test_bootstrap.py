"""
Test running bootstrap script in different circumstances
"""
import subprocess
from textwrap import dedent

def run_bootstrap(container_name, image):
    # stop container if it is already running
    subprocess.run([
        'docker', 'rm', '-f', container_name
    ])
    
    # Start a detached Ubuntu 16.04 container
    subprocess.check_call([
        'docker', 'run', '--detach', '--name', container_name, image,
        '/bin/bash', '-c', 'sleep 1000s'
    ])
    # Install python3 inside the ubuntu container
    # There is no trusted Ubuntu+Python3 container we can use
    subprocess.check_output([
        'docker', 'exec', container_name, 'apt-get', 'update'
    ])
    subprocess.check_output([
        'docker', 'exec', container_name, 'apt-get', 'install', '--yes', 'python3'
    ])
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
    ], check=False, stdout=subprocess.PIPE, encoding='utf-8')

def test_ubuntu_too_old():
    """
    Error with a useful message when running in older Ubuntu
    """
    output = run_bootstrap('old-distro-test', 'ubuntu:16.04')
    assert output.stdout == 'The Littlest JupyterHub requires Ubuntu 18.04 or higher\n'
    assert output.returncode == 1


def test_inside_plain_docker():
    output = run_bootstrap('plain-docker-test', 'ubuntu:18.04')
    assert output.stdout.strip() == dedent("""
        Systemd is required to run TLJH
        Running inside a plain docker container isn't supported
        For local development, see http://tljh.jupyter.org/en/latest/contributing/dev-setup.html
    """).strip()
    assert output.returncode == 1
