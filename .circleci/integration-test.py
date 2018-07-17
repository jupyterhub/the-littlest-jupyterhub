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
        image_name
    ])


def remove_systemd_container(container_name):
    """
    Stop & remove docker container if it exists.
    """
    try:
        subprocess.check_output([
            'docker', 'inspect', container_name
        ])
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
    subprocess.check_call([
        'docker', 'exec',
        '-it', container_name,
        '/bin/bash', '-c', cmd
    ])


def copy_to_container(container_name, src_path, dest_path):
    """
    Copy files from src_path to dest_path inside container_name
    """
    subprocess.check_call([
        'docker', 'cp',
        src_path, f'{container_name}:{dest_path}'
    ])


def main():
    argparser = argparse.ArgumentParser()
    subparsers = argparser.add_subparsers(dest='action')

    subparsers.add_parser('build-image')
    subparsers.add_parser('start-container')
    subparsers.add_parser('stop-container')
    subparsers.add_parser('run').add_argument(
        'command',
    )
    copy_parser = subparsers.add_parser('copy')
    copy_parser.add_argument('src')
    copy_parser.add_argument('dest')

    args = argparser.parse_args()

    image_name = 'tljh-systemd'
    container_name = 'tljh-ci-run'
    source_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), os.pardir, 'integration-tests')
    )

    if args.action == 'build-image':
        build_systemd_image(image_name, source_path)
    elif args.action == 'start-container':
        run_systemd_image(image_name, container_name)
    elif args.action == 'stop-container':
        remove_systemd_container(container_name)
    elif args.action == 'run':
        run_container_command(container_name, args.command)
    elif args.action == 'copy':
        copy_to_container(container_name, args.src, args.dest)


if __name__ == '__main__':
    main()
