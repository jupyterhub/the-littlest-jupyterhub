"""
Test running on non-supported distros
"""
import subprocess

def test_ubuntu_too_old():
    container_name = 'old-distro-test'

    # stop container if it is already running
    subprocess.run([
        'docker', 'rm', '-f', container_name
    ])
    
    # Start a detached Ubuntu 16.04 container
    subprocess.check_call([
        'docker', 'run', '--detach', '--name', container_name, 'ubuntu:16.04', 
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

    # Run bootstrap script, validate that it fails appropriately
    output = subprocess.run([
        'docker', 'exec', '-i', container_name,
        'python3', '/srv/bootstrap/bootstrap.py'
    ], check=False, stdout=subprocess.PIPE, encoding='utf-8')
    assert output.stdout == 'The Littlest JupyterHub requires Ubuntu 18.04 or higher\n'
    assert output.returncode == 1