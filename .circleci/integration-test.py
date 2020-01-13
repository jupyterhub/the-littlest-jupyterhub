#!/usr/bin/env python3
import argparse
import subprocess
import os


def build_systemd_image(image_name, source_path):
    """
    Build docker image with systemd at source_path.

    Built image is tagged with image_name
    """
    subprocess.check_call([
        'docker', 'build', '-t', image_name, source_path
    ])


def run_systemd_image(image_name, container_name):
    """
    Run docker image with systemd

    Image named image_name should be built with build_systemd_image.

    Container named container_name will be started.
    """
    subprocess.check_call([
        'docker', 'run',
        '--privileged',
        '--mount', 'type=bind,source=/sys/fs/cgroup,target=/sys/fs/cgroup',
        '--detach',
        '--name', container_name,
        # This is the minimum VM size we support. JupyterLab extensions seem
        # to need at least this much RAM to build. Boo?
        # If we change this, need to change all other references to this number.
        '--memory', '1G',
        image_name
    ])


def stop_container(container_name):
    """
    Stop & remove docker container if it exists.
    """
    try:
        subprocess.check_output([
            'docker', 'inspect', container_name
        ], stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError:
        # No such container exists, nothing to do
        return
    subprocess.check_call([
        'docker', 'rm', '-f', container_name
    ])


def run_container_command(container_name, cmd):
    """
    Run cmd in a running container with a bash shell
    """
    proc = subprocess.run([
        'docker', 'exec',
        '-it', container_name,
        '/bin/bash', '-c', cmd
    ], check=True)


def copy_to_container(container_name, src_path, dest_path):
    """
    Copy files from src_path to dest_path inside container_name
    """
    subprocess.check_call([
        'docker', 'cp',
        src_path, f'{container_name}:{dest_path}'
    ])


def run_test(image_name, test_name, test_files, installer_args):
    """
    Wrapper that sets up tljh with installer_args & runs test_name
    """
    stop_container(test_name)
    run_systemd_image(image_name, test_name)

    source_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), os.pardir)
    )

    copy_to_container(test_name, source_path, '/srv/src')
    run_container_command(
        test_name,
        f'python3 /srv/src/bootstrap/bootstrap.py {installer_args}'
    )
    run_container_command(
        test_name,
        'python3 -m pip install -r /srv/src/integration-tests/requirements.txt'
    )
    run_container_command(
        test_name,
        'python3 -m pytest -v {}'.format(
            ' '.join([os.path.join('/srv/src/integration-tests/', f) for f in test_files])
        )
    )


def show_logs(container_name):
    """
    Print logs from inside container to stdout
    """
    run_container_command(
        container_name,
        'journalctl --no-pager'
    )
    run_container_command(
        container_name,
        'systemctl --no-pager status jupyterhub traefik'
    )

def main():
    argparser = argparse.ArgumentParser()
    subparsers = argparser.add_subparsers(dest='action')

    subparsers.add_parser('build-image')
    subparsers.add_parser('stop-container').add_argument(
        'container_name'
    )
    subparsers.add_parser('start-container').add_argument(
        'container_name'
    )
    run_parser = subparsers.add_parser('run')
    run_parser.add_argument('container_name')
    run_parser.add_argument('command')

    copy_parser = subparsers.add_parser('copy')
    copy_parser.add_argument('container_name')
    copy_parser.add_argument('src')
    copy_parser.add_argument('dest')

    run_test_parser = subparsers.add_parser('run-test')
    run_test_parser.add_argument('--installer-args', default='')
    run_test_parser.add_argument('test_name')
    run_test_parser.add_argument('test_files', nargs='+')

    show_logs_parser = subparsers.add_parser('show-logs')
    show_logs_parser.add_argument('container_name')

    args = argparser.parse_args()

    image_name = 'tljh-systemd'

    if args.action == 'run-test':
        run_test(image_name, args.test_name, args.test_files, args.installer_args)
    elif args.action == 'show-logs':
        show_logs(args.container_name)
    elif args.action == 'run':
        run_container_command(args.container_name, args.command)
    elif args.action == 'copy':
        copy_to_container(args.container_name, args.src, args.dest)
    elif args.action == 'start-container':
        run_systemd_image(image_name, args.container_name)
    elif args.action == 'stop-container':
        stop_container(args.container_name)
    elif args.action == 'build-image':
        build_systemd_image(image_name, 'integration-tests')


if __name__ == '__main__':
    main()
