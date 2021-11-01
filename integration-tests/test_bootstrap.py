"""
Test running bootstrap script in different circumstances
"""
import concurrent.futures
import os
import subprocess
import time


def install_pkgs(container_name, show_progress_page):
    # Install python3 inside the ubuntu container
    # There is no trusted Ubuntu+Python3 container we can use
    pkgs = ["python3"]
    if show_progress_page:
        pkgs += ["systemd", "git", "curl"]
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


# FIXME: Refactor this function to easier to understand using the following
#        parameters
#
# - param: container_apt_packages
# - param: bootstrap_tljh_source
#   - local: copies local tljh repo to container and configures bootstrap to
#            install tljh from copied repo
#   - github: configures bootstrap to install tljh from the official github repo
#   - <pip spec>: configures bootstrap to install tljh from any given remote location
# - param: bootstrap_flags
#
# FIXME: Consider stripping logic in this file to only testing if the bootstrap
#        script successfully detects the too old Ubuntu version and the lack of
#        systemd. The remaining test named test_progress_page could rely on
#        running against the systemd container that cab be built by
#        integration-test.py.
#
def run_bootstrap_after_preparing_container(
    container_name, image, show_progress_page=False
):
    """
    1. Stops old container
    2. Starts --detached container
    3. Installs apt packages in container
    4. Two situations

        A) limited test (--show-progress-page=false)
        - Copies ./bootstrap/ folder content to container /srv/src
        - Runs copied bootstrap/bootstrap.py without flags

        B) full test (--show-progress-page=true)
        - Copies ./ folder content to the container /srv/src
        - Runs copied bootstrap/bootstrap.py with environment variables
            - TLJH_BOOTSTRAP_DEV=yes
              This makes --editable be used when installing the tljh package
            - TLJH_BOOTSTRAP_PIP_SPEC=/srv/src
              This makes us install tljh from the given location instead of from
              github.com/jupyterhub/the-littlest-jupyterhub
    """
    # stop container if it is already running
    subprocess.run(["docker", "rm", "-f", container_name])

    # Start a detached container
    subprocess.check_call(
        [
            "docker",
            "run",
            "--env=DEBIAN_FRONTEND=noninteractive",
            "--detach",
            f"--name={container_name}",
            image,
            "/bin/bash",
            "-c",
            "sleep 1000s",
        ]
    )

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
    output = run_bootstrap_after_preparing_container("old-distro-test", "ubuntu:16.04")
    assert output.stdout == "The Littlest JupyterHub requires Ubuntu 18.04 or higher\n"
    assert output.returncode == 1


def test_inside_no_systemd_docker():
    output = run_bootstrap_after_preparing_container(
        "plain-docker-test",
        f"ubuntu:{os.getenv('UBUNTU_VERSION', '20.04')}",
    )
    assert "Systemd is required to run TLJH" in output.stdout
    assert output.returncode == 1


def verify_progress_page(expected_status_code, timeout):
    progress_page_status = False
    start = time.time()
    while not progress_page_status and (time.time() - start < timeout):
        try:
            resp = subprocess.check_output(
                [
                    "docker",
                    "exec",
                    "progress-page",
                    "curl",
                    "-i",
                    "http://localhost/index.html",
                ]
            )
            if b"HTTP/1.0 200 OK" in resp:
                progress_page_status = True
                break
        except Exception as e:
            time.sleep(2)
            continue

    return progress_page_status


def test_progress_page():
    with concurrent.futures.ThreadPoolExecutor() as executor:
        installer = executor.submit(
            run_bootstrap_after_preparing_container,
            "progress-page",
            f"ubuntu:{os.getenv('UBUNTU_VERSION', '20.04')}",
            True,
        )

        # Check if progress page started
        started = verify_progress_page(expected_status_code=200, timeout=120)
        assert started

        # This will fail start tljh but should successfully get to the point
        # Where it stops the progress page server.
        output = installer.result()

        # Check if progress page stopped
        assert "Progress page server stopped successfully." in output.stdout
