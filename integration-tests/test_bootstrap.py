"""
Test running bootstrap script in different circumstances
"""
import concurrent.futures
import os
import requests
import subprocess
from textwrap import dedent
import time


def start_container(container_name, image, show_progress_page):
    run_flags = [
        "--detach",
        "--name",
        container_name,
        image,
        "/bin/bash",
        "-c",
        "sleep 1000s",
    ]
    if show_progress_page:
        # Use port-forwarding to be able to access the progress page when it starts
        run_flags = ["--publish", "12000:80"] + run_flags

    # Start a detached container
    subprocess.check_call(["docker", "run"] + run_flags)


def install_pkgs(container_name, show_progress_page):
    # Install python3 inside the ubuntu container
    # There is no trusted Ubuntu+Python3 container we can use
    pkgs = ["python3"]
    if show_progress_page:
        pkgs += ["systemd", "git"]
        # Create the sudoers dir, so that the installer succesfully gets to the
        # point of starting jupyterhub and stopping the progress page server.
        subprocess.check_output(
            ["docker", "exec", container_name, "mkdir", "-p", "etc/sudoers.d"]
        )

    subprocess.check_output(["docker", "exec", container_name, "apt-get", "update"])
    subprocess.check_output(
        ["docker", "exec", container_name, "apt-get", "install", "--yes"] + pkgs
    )


def get_bootstrap_script_location(container_name, show_progress_page):
    # Copy only the bootstrap script to container when progress page not enabled, to be faster
    source_path = "bootstrap/"
    bootstrap_script = "/srv/src/bootstrap.py"
    if show_progress_page:
        source_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), os.pardir)
        )
        bootstrap_script = "/srv/src/bootstrap/bootstrap.py"

    subprocess.check_call(["docker", "cp", source_path, f"{container_name}:/srv/src"])
    return bootstrap_script


def run_bootstrap(container_name, image, show_progress_page=False):
    # stop container if it is already running
    subprocess.run(["docker", "rm", "-f", container_name])

    start_container(container_name, image, show_progress_page)
    install_pkgs(container_name, show_progress_page)

    bootstrap_script = get_bootstrap_script_location(container_name, show_progress_page)

    exec_flags = ["-i", container_name, "python3", bootstrap_script]
    if show_progress_page:
        exec_flags = (
            ["-e", "TLJH_BOOTSTRAP_DEV=yes", "-e", "TLJH_BOOTSTRAP_PIP_SPEC=/srv/src"]
            + exec_flags
            + ["--show-progress-page"]
        )

    # Run bootstrap script, return the output
    return subprocess.run(
        ["docker", "exec"] + exec_flags,
        check=False,
        stdout=subprocess.PIPE,
        encoding="utf-8",
    )


def test_ubuntu_too_old():
    """
    Error with a useful message when running in older Ubuntu
    """
    output = run_bootstrap("old-distro-test", "ubuntu:16.04")
    assert output.stdout == "The Littlest JupyterHub requires Ubuntu 18.04 or higher\n"
    assert output.returncode == 1


def test_inside_no_systemd_docker():
    output = run_bootstrap("plain-docker-test", "ubuntu:18.04")
    assert (
        output.stdout.strip()
        == dedent(
            """
        Systemd is required to run TLJH
        Running inside a docker container without systemd isn't supported
        We recommend against running a production TLJH instance inside a docker container
        For local development, see http://tljh.jupyter.org/en/latest/contributing/dev-setup.html
    """
        ).strip()
    )
    assert output.returncode == 1


def verify_progress_page(expected_status_code, timeout):
    progress_page_status = False
    start = time.time()
    while not progress_page_status and (time.time() - start < timeout):
        try:
            resp = requests.get("http://127.0.0.1:12000/index.html")
            if resp.status_code == expected_status_code:
                progress_page_status = True
                break
        except Exception as e:
            time.sleep(2)
            continue

    return progress_page_status


def test_progress_page():
    with concurrent.futures.ThreadPoolExecutor() as executor:
        installer = executor.submit(
            run_bootstrap, "progress-page", "ubuntu:18.04", True
        )

        # Check if progress page started
        started = verify_progress_page(expected_status_code=200, timeout=120)
        assert started

        # This will fail start tljh but should successfully get to the point
        # Where it stops the progress page server.
        output = installer.result()

        # Check if progress page stopped
        assert "Progress page server stopped successfully." in output.stdout
