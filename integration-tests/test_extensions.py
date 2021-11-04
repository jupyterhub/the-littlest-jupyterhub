import subprocess


def test_serverextensions():
    """
    Validate serverextensions we want are installed
    """
    # jupyter-serverextension writes to stdout and stderr weirdly
    proc = subprocess.run(
        ["/opt/tljh/user/bin/jupyter-serverextension", "list", "--sys-prefix"],
        stderr=subprocess.PIPE,
    )

    extensions = [
        "jupyterlab 3.",
        "nbgitpuller 1.",
        "nteract_on_jupyter 2.1.",
        "jupyter_resource_usage",
    ]

    for e in extensions:
        assert e in proc.stderr.decode()


def test_nbextensions():
    """
    Validate nbextensions we want are installed & enabled
    """
    # jupyter-nbextension writes to stdout and stderr weirdly
    proc = subprocess.run(
        ["/opt/tljh/user/bin/jupyter-nbextension", "list", "--sys-prefix"],
        stderr=subprocess.PIPE,
        stdout=subprocess.PIPE,
    )

    extensions = [
        "jupyter_resource_usage/main",
        # This is what ipywidgets nbextension is called
        "jupyter-js-widgets/extension",
    ]

    for e in extensions:
        assert f"{e} \x1b[32m enabled \x1b[0m" in proc.stdout.decode()

    # Ensure we have 'OK' messages in our stdout, to make sure everything is importable
    assert proc.stderr.decode() == "      - Validating: \x1b[32mOK\x1b[0m\n" * len(
        extensions
    )
