#!/usr/bin/env python3
import argparse
import subprocess
import os


def build_systemd_image(image_name, source_path, build_args=None):
    """
    Build docker image with systemd at source_path.

    Built image is tagged with image_name
    """
    cmd = ["docker", "build", f"-t={image_name}", source_path]
    if build_args:
        cmd.extend([f"--build-arg={ba}" for ba in build_args])
    subprocess.check_call(cmd)


def run_systemd_image(image_name, container_name, bootstrap_pip_spec):
    """
    Run docker image with systemd

    Image named image_name should be built with build_systemd_image.

    Container named container_name will be started.
    """
    cmd = [
        "docker",
        "run",
        "--privileged",
        "--mount=type=bind,source=/sys/fs/cgroup,target=/sys/fs/cgroup",
        "--detach",
        f"--name={container_name}",
        # A bit less than 1GB to ensure TLJH runs on 1GB VMs.
        # If this is changed all docs references to the required memory must be changed too.
        "--memory=900m",
    ]

    if bootstrap_pip_spec:
        cmd.append("-e")
        cmd.append(f"TLJH_BOOTSTRAP_PIP_SPEC={bootstrap_pip_spec}")

    cmd.append(image_name)

    subprocess.check_call(cmd)


def stop_container(container_name):
    """
    Stop & remove docker container if it exists.
    """
    try:
        subprocess.check_output(
            ["docker", "inspect", container_name], stderr=subprocess.STDOUT
        )
    except subprocess.CalledProcessError:
        # No such container exists, nothing to do
        return
    subprocess.check_call(["docker", "rm", "-f", container_name])


def run_container_command(container_name, cmd):
    """
    Run cmd in a running container with a bash shell
    """
    proc = subprocess.run(
        ["docker", "exec", "-t", container_name, "/bin/bash", "-c", cmd], check=True
    )


def copy_to_container(container_name, src_path, dest_path):
    """
    Copy files from src_path to dest_path inside container_name
    """
    subprocess.check_call(["docker", "cp", src_path, f"{container_name}:{dest_path}"])


def run_test(
    image_name, test_name, bootstrap_pip_spec, test_files, upgrade, installer_args
):
    """
    Wrapper that sets up tljh with installer_args & runs test_name
    """
    stop_container(test_name)
    run_systemd_image(image_name, test_name, bootstrap_pip_spec)

    source_path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))

    copy_to_container(test_name, os.path.join(source_path, "bootstrap/."), "/srv/src")
    copy_to_container(
        test_name, os.path.join(source_path, "integration-tests/"), "/srv/src"
    )

    # These logs can be very relevant to debug a container startup failure
    print(f"--- Start of logs from the container: {test_name}")
    print(subprocess.check_output(["docker", "logs", test_name]).decode())
    print(f"--- End of logs from the container: {test_name}")

    # Install TLJH from the default branch first to test upgrades
    if upgrade:
        run_container_command(
            test_name, "curl -L https://tljh.jupyter.org/bootstrap.py | python3 -"
        )

    run_container_command(test_name, f"python3 /srv/src/bootstrap.py {installer_args}")

    # Install pkgs from requirements in hub's pip, where
    # the bootstrap script installed the others
    run_container_command(
        test_name,
        "/opt/tljh/hub/bin/python3 -m pip install -r /srv/src/integration-tests/requirements.txt",
    )
    run_container_command(
        test_name,
        # We abort pytest after two failures as a compromise between wanting to
        # avoid a flood of logs while still understanding if multiple tests
        # would fail.
        "/opt/tljh/hub/bin/python3 -m pytest --verbose --maxfail=2 --color=yes --durations=10 --capture=no {}".format(
            " ".join(
                [os.path.join("/srv/src/integration-tests/", f) for f in test_files]
            )
        ),
    )


def show_logs(container_name):
    """
    Print logs from inside container to stdout
    """
    run_container_command(container_name, "journalctl --no-pager")
    run_container_command(
        container_name, "systemctl --no-pager status jupyterhub traefik"
    )


def main():
    argparser = argparse.ArgumentParser()
    subparsers = argparser.add_subparsers(dest="action")

    build_image_parser = subparsers.add_parser("build-image")
    build_image_parser.add_argument(
        "--build-arg",
        action="append",
        dest="build_args",
    )

    subparsers.add_parser("stop-container").add_argument("container_name")

    subparsers.add_parser("start-container").add_argument("container_name")

    run_parser = subparsers.add_parser("run")
    run_parser.add_argument("container_name")
    run_parser.add_argument("command")

    copy_parser = subparsers.add_parser("copy")
    copy_parser.add_argument("container_name")
    copy_parser.add_argument("src")
    copy_parser.add_argument("dest")

    run_test_parser = subparsers.add_parser("run-test")
    run_test_parser.add_argument("--installer-args", default="")
    run_test_parser.add_argument("--upgrade", action="store_true")
    run_test_parser.add_argument(
        "--bootstrap-pip-spec", nargs="?", default="", type=str
    )
    run_test_parser.add_argument("test_name")
    run_test_parser.add_argument("test_files", nargs="+")

    show_logs_parser = subparsers.add_parser("show-logs")
    show_logs_parser.add_argument("container_name")

    args = argparser.parse_args()

    image_name = "tljh-systemd"

    if args.action == "run-test":
        run_test(
            image_name,
            args.test_name,
            args.bootstrap_pip_spec,
            args.test_files,
            args.upgrade,
            args.installer_args,
        )
    elif args.action == "show-logs":
        show_logs(args.container_name)
    elif args.action == "run":
        run_container_command(args.container_name, args.command)
    elif args.action == "copy":
        copy_to_container(args.container_name, args.src, args.dest)
    elif args.action == "start-container":
        run_systemd_image(image_name, args.container_name, args.bootstrap_pip_spec)
    elif args.action == "stop-container":
        stop_container(args.container_name)
    elif args.action == "build-image":
        build_systemd_image(image_name, "integration-tests", args.build_args)


if __name__ == "__main__":
    main()
