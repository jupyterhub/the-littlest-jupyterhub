"""
This test file tests bootstrap.py ability to

- error verbosely for old ubuntu
- error verbosely for no systemd
- start and provide a progress page web server

FIXME: The last test stands out and could be part of the other tests, and the
       first two could be more like unit tests. Ideally, this file is
       significantly reduced.
"""

import concurrent.futures
import os
import subprocess
import time

GIT_REPO_PATH = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
BASE_IMAGE = os.getenv("BASE_IMAGE", "ubuntu:20.04")


def _stop_container():
    """
    Stops a container if its already running.
    """
    subprocess.run(
        ["docker", "rm", "--force", "test-bootstrap"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


def _run_bootstrap_in_container(image, complete_setup=True):
    """
    1. (Re-)starts a container named test-bootstrap based on image, mounting
       local git repo and exposing port 8080 to the containers port 80.
    2. Installs python3, systemd, git, and curl in container
    3. Runs bootstrap/bootstrap.py in container to install the mounted git
       repo's tljh package in --editable mode.
    """
    _stop_container()

    # Start a detached container
    subprocess.check_output(
        [
            "docker",
            "run",
            "--env=DEBIAN_FRONTEND=noninteractive",
            "--env=TLJH_BOOTSTRAP_DEV=yes",
            "--env=TLJH_BOOTSTRAP_PIP_SPEC=/srv/src",
            f"--volume={GIT_REPO_PATH}:/srv/src",
            "--publish=8080:80",
            "--detach",
            "--name=test-bootstrap",
            image,
            "bash",
            "-c",
            "sleep 300s",
        ]
    )

    run = ["docker", "exec", "-i", "test-bootstrap"]
    subprocess.check_output(run + ["apt-get", "update"])
    subprocess.check_output(run + ["apt-get", "install", "--yes", "python3"])
    if complete_setup:
        subprocess.check_output(
            run + ["apt-get", "install", "--yes", "systemd", "git", "curl"]
        )

    run_bootstrap = run + [
        "python3",
        "/srv/src/bootstrap/bootstrap.py",
        "--show-progress-page",
    ]

    # Run bootstrap script inside detached container, return the output
    return subprocess.run(
        run_bootstrap,
        text=True,
        capture_output=True,
    )


def test_ubuntu_too_old():
    """
    Error with a useful message when running in older Ubuntu
    """
    output = _run_bootstrap_in_container("ubuntu:20.04", False)
    _stop_container()
    assert output.stdout == "The Littlest JupyterHub requires Ubuntu 22.04 or higher\n"
    assert output.returncode == 1


def test_no_systemd():
    output = _run_bootstrap_in_container("ubuntu:22.04", False)
    assert "Systemd is required to run TLJH" in output.stdout
    assert output.returncode == 1


def _wait_for_progress_page_response(expected_status_code, timeout):
    start = time.time()
    while time.time() - start < timeout:
        try:
            resp = subprocess.check_output(
                [
                    "curl",
                    "--include",
                    "http://localhost:8080/index.html",
                ],
                text=True,
                stderr=subprocess.DEVNULL,
            )
            if "HTTP/1.0 200 OK" in resp:
                return True
        except Exception:
            pass
        time.sleep(1)

    return False


def test_show_progress_page():
    with concurrent.futures.ThreadPoolExecutor() as executor:
        run_bootstrap_job = executor.submit(_run_bootstrap_in_container, BASE_IMAGE)

        # Check that the bootstrap script started the web server reporting
        # progress successfully responded.
        success = _wait_for_progress_page_response(
            expected_status_code=200, timeout=180
        )
        if success:
            # Let's terminate the test here and save a minute or so in test
            # executation time, because we can know that the will be stopped
            # successfully in other tests as otherwise traefik won't be able to
            # start and use the same port for example.
            return

        # Now await an expected failure to startup JupyterHub by tljh.installer,
        # which should have taken over the work started by the bootstrap script.
        #
        # This failure is expected to occur in
        # tljh.installer.ensure_jupyterhub_service calling systemd.reload_daemon
        # like this:
        #
        # > System has not been booted with systemd as init system (PID 1).
        # > Can't operate.
        #
        output = run_bootstrap_job.result()
        print(output.stdout)
        print(output.stderr)

        # At this point we should be able to see that tljh.installer
        # intentionally stopped the web server reporting progress as the port
        # were about to become needed by Traefik.
        assert "Progress page server stopped successfully." in output.stdout
        assert success
