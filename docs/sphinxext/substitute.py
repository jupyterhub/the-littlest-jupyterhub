"""
Substitute placeholder values in the docs with values set in conf.py.
"""

def ubuntu_version_sub(app, docname, source):
    """
    Replace `||UBUNTU_PREVIOUS_VERSION||` and `||UBUNTU_LATEST_VERSION||` with the supported versions of Ubuntu.

    As new versions of Ubuntu are released, update the `ext_ubuntu_latest_version` and `ext_ubuntu_previous_version` in the `conf.py`.
    """
    if app.config.ext_ubuntu_latest_version != "" and app.config.ext_ubuntu_previous_version != "":
        src = source[0]
        source[0] = (src
            .replace("||UBUNTU_PREVIOUS_VERSION||", app.config.ext_ubuntu_latest_version)
            .replace("||UBUNTU_LATEST_VERSION||", app.config.ext_ubuntu_previous_version)
        )


def setup(app):
    app.connect("source-read", ubuntu_version_sub)
    app.add_config_value("ext_ubuntu_latest_version", "", "env")
    app.add_config_value("ext_ubuntu_previous_version", "", "env")