#!/usr/bin/env python3
import argparse
import functools
import os
import subprocess
import time
from shutil import which

GIT_REPO_PATH = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
TEST_IMAGE_NAME = "test-systemd"


@functools.lru_cache
def _get_container_runtime_cli():
    runtimes = ["docker", "podman"]
    for runtime in runtimes:
        if which(runtime):
            return runtime
    raise RuntimeError(f"No container runtime CLI found, tried: {' '.join(runtimes)}")


def _cli(args, log_failure=True):
    cmd = [_get_container_runtime_cli(), *args]
    try:
        return subprocess.check_output(cmd, text=True, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError:
        if log_failure:
            print(f"{cmd} failed!", flush=True)
        raise


def _await_container_startup(container_name, timeout=60):
    """
    Await container to become ready, as checked by attempting to run a basic
    command (id) inside it.
    """
    start = time.time()
    while True:
        try:
            _cli(["exec", "-t", container_name, "id"], log_failure=False)
            return
        except subprocess.CalledProcessError:
            if time.time() - start > timeout:
                inspect = ""
                logs = ""
                try:
                    inspect = _cli(["inspect", container_name], log_failure=False)
                except subprocess.CalledProcessError as e:
                    inspect = e.output
                try:
                    logs = _cli(["logs", container_name], log_failure=False)
                except subprocess.CalledProcessError as e:
                    logs = e.output
                raise RuntimeError(
                    f"Container {container_name} failed to start! Debugging info follows...\n\n"
                    f"> docker inspect {container_name}\n"
                    "----------------------------------------\n"
                    f"{inspect}\n"
                    f"> docker logs {container_name}\n"
                    "----------------------------------------\n"
                    f"{logs}\n"
                )
            time.sleep(1)


def build_image(build_args=None):
    """
    Build Dockerfile with systemd in the integration-tests folder to run tests
    from.
    """
    cmd = [
        _get_container_runtime_cli(),
        "build",
        f"--tag={TEST_IMAGE_NAME}",
        "integration-tests",
    ]
    if build_args:
        cmd.extend([f"--build-arg={ba}" for ba in build_args])

    subprocess.run(cmd, check=True, text=True)


def start_container(container_name, bootstrap_pip_spec):
    """
    Starts a container based on an image expected to start systemd.
    """
    cmd = [
        "run",
        "--rm",
        "--detach",
        "--privileged",
        f"--name={container_name}",
        # A bit less than 1GB to ensure TLJH runs on 1GB VMs.
        # If this is changed all docs references to the required memory must be changed too.
        "--memory=900m",
    ]
    if bootstrap_pip_spec:
        cmd.append(f"--env=TLJH_BOOTSTRAP_PIP_SPEC={bootstrap_pip_spec}")
    else:
        cmd.append("--env=TLJH_BOOTSTRAP_DEV=yes")
        cmd.append("--env=TLJH_BOOTSTRAP_PIP_SPEC=/srv/src")
    cmd.append(TEST_IMAGE_NAME)

    return _cli(cmd)


def stop_container(container_name):
    """
    Stop and remove docker container if it exists.
    """
    try:
        return _cli(["rm", "--force", container_name], log_failure=False)
    except subprocess.CalledProcessError:
        pass


def run_command(container_name, command):
    """
    Run a bash command in a running container and error if it fails
    """
    cmd = [
        _get_container_runtime_cli(),
        "exec",
        "-t",
        container_name,
        "/bin/bash",
        "-c",
        command,
    ]
    print(f"\nRunning: {cmd}\n----------------------------------------", flush=True)
    subprocess.run(cmd, check=True, text=True)


def copy_to_container(container_name, src_path, dest_path):
    """
    Copy files from a path on the local file system to a destination in a
    running container
    """
    _cli(["cp", src_path, f"{container_name}:{dest_path}"])


def run_test(
    container_name,
    bootstrap_pip_spec,
    test_files,
    upgrade_from,
    installer_args,
):
    """
    (Re-)starts a named container with given (Systemd based) image, then runs
    the bootstrap script inside it to setup tljh with installer_args.

    Thereafter, source files are copied to the container and
    """
    stop_container(container_name)
    start_container(container_name, bootstrap_pip_spec)
    _await_container_startup(container_name)
    copy_to_container(container_name, GIT_REPO_PATH, "/srv/src")

    # To test upgrades, we run a bootstrap.py script two times instead of one,
    # where the initial run first installs some older version.
    #
    # We want to support testing a PR by upgrading from "main", "latest" (latest
    # released version), and from a previous major-like version.
    #
    if upgrade_from:
        command = f"python3 /srv/src/bootstrap/bootstrap.py --version={upgrade_from}"
        run_command(container_name, command)

        # show user environment
        command = "/opt/tljh/user/bin/mamba list"
        run_command(container_name, command)

    command = f"python3 /srv/src/bootstrap/bootstrap.py {' '.join(installer_args)}"
    run_command(container_name, command)

    # show user environment (again if upgrade)
    command = "/opt/tljh/user/bin/mamba list"
    run_command(container_name, command)

    # Install pkgs from requirements in hub's pip, where
    # the bootstrap script installed the others
    command = "/opt/tljh/hub/bin/python3 -m pip install -r /srv/src/integration-tests/requirements.txt"
    run_command(container_name, command)

    # show hub environment
    command = "/opt/tljh/hub/bin/python3 -m pip freeze"
    run_command(container_name, command)

    # run tests
    test_files = " ".join([f"/srv/src/integration-tests/{f}" for f in test_files])
    command = f"/opt/tljh/hub/bin/python3 -m pytest {test_files}"
    run_command(container_name, command)


def show_logs(container_name):
    """
    Print jupyterhub and traefik status and logs from both.

    tljh logs ref: https://tljh.jupyter.org/en/latest/troubleshooting/logs.html
    """
    run_command(container_name, "systemctl --no-pager status jupyterhub traefik")
    run_command(container_name, "journalctl --no-pager -u jupyterhub")
    run_command(container_name, "journalctl --no-pager -u traefik")


def main():
    argparser = argparse.ArgumentParser()
    subparsers = argparser.add_subparsers(dest="action")

    build_image_parser = subparsers.add_parser("build-image")
    build_image_parser.add_argument("--build-arg", action="append", dest="build_args")

    start_container_parser = subparsers.add_parser("start-container")
    start_container_parser.add_argument("container_name")

    stop_container_parser = subparsers.add_parser("stop-container")
    stop_container_parser.add_argument("container_name")

    run_parser = subparsers.add_parser("run")
    run_parser.add_argument("container_name")
    run_parser.add_argument("command")

    copy_parser = subparsers.add_parser("copy")
    copy_parser.add_argument("container_name")
    copy_parser.add_argument("src")
    copy_parser.add_argument("dest")

    run_test_parser = subparsers.add_parser("run-test")
    run_test_parser.add_argument("--installer-args", action="append")
    run_test_parser.add_argument("--upgrade-from", default="")
    run_test_parser.add_argument("--bootstrap-pip-spec", default="/srv/src")
    run_test_parser.add_argument("container_name")
    run_test_parser.add_argument("test_files", nargs="+")

    show_logs_parser = subparsers.add_parser("show-logs")
    show_logs_parser.add_argument("container_name")

    args = argparser.parse_args()

    if args.action == "build-image":
        build_image(args.build_args)
    elif args.action == "start-container":
        start_container(args.container_name, args.bootstrap_pip_spec)
    elif args.action == "stop-container":
        stop_container(args.container_name)
    elif args.action == "run":
        run_command(args.container_name, args.command)
    elif args.action == "copy":
        copy_to_container(args.container_name, args.src, args.dest)
    elif args.action == "run-test":
        run_test(
            args.container_name,
            args.bootstrap_pip_spec,
            args.test_files,
            args.upgrade_from,
            args.installer_args,
        )
    elif args.action == "show-logs":
        show_logs(args.container_name)


if __name__ == "__main__":
    main()
