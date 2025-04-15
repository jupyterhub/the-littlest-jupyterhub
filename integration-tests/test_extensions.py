import re
import subprocess


def test_serverextensions():
    """
    Validate serverextensions we want are installed
    """
    # jupyter-serverextension writes to stdout and stderr weirdly
    proc = subprocess.run(
        ["/opt/tljh/user/bin/jupyter-server", "extension", "list", "--sys-prefix"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )

    output = proc.stdout.decode()

    extensions = [
        "jupyterlab",
        "nbgitpuller",
        "jupyter_resource_usage",
    ]

    for e in extensions:
        assert e in output, f"'{e}' not found in server extensions: {output}"


def test_labextensions():
    """
    Validate JupyterLab extensions we want are installed & enabled
    """
    # jupyter-labextension writes to stdout and stderr weirdly
    proc = subprocess.run(
        ["/opt/tljh/user/bin/jupyter-labextension", "list"],
        capture_output=True,
    )

    extensions = [
        "@jupyter-server/resource-usage",
        # This is what ipywidgets lab extension is called
        "@jupyter-widgets/jupyterlab-manager",
    ]

    for e in extensions:
        # jupyter labextension lists outputs to stderr
        out = proc.stderr.decode()
        enabled_ok_pattern = re.compile(rf"{e}.*enabled.*OK")
        matches = enabled_ok_pattern.search(out)
        assert matches is not None
