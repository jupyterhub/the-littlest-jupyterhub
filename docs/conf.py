# Configuration file for Sphinx to build our documentation to HTML.
#
# Configuration reference: https://www.sphinx-doc.org/en/master/usage/configuration.html
#
import datetime

# -- Project information -----------------------------------------------------
# ref: https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
#
project = "The Littlest JupyterHub"
copyright = f"{datetime.date.today().year}, Project Jupyter Contributors"
author = "Project Jupyter Contributors"


# -- General Sphinx configuration ---------------------------------------------------
# ref: https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration
#
# Add any Sphinx extension module names here, as strings. They can be extensions
# coming with Sphinx (named 'sphinx.ext.*') or your custom ones.
#
extensions = [
    "sphinx_copybutton",
    "sphinxext.opengraph",
    "sphinxext.rediraffe",
    "myst_parser",
]
root_doc = "index"
source_suffix = [".md"]


# -- Options for HTML output -------------------------------------------------
# ref: https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output
#
html_logo = "_static/images/logo/logo.png"
html_favicon = "_static/images/logo/favicon.ico"
html_static_path = ["_static"]

# pydata_sphinx_theme reference: https://pydata-sphinx-theme.readthedocs.io/en/stable/index.html
html_theme = "pydata_sphinx_theme"
html_theme_options = {
    "navigation_with_keys": False,
    "icon_links": [
        {
            "name": "GitHub",
            "url": "https://github.com/jupyterhub/the-littlest-jupyterhub",
            "icon": "fab fa-github-square",
        },
        {
            "name": "Discourse",
            "url": "https://discourse.jupyter.org/c/jupyterhub/tljh/13",
            "icon": "fab fa-discourse",
        },
    ],
    "use_edit_page_button": True,
}
html_context = {
    "github_user": "jupyterhub",
    "github_repo": "the-littlest-jupyterhub",
    "github_version": "main",
    "doc_path": "docs",
}

# -- MyST configuration ------------------------------------------------------
# ref: https://myst-parser.readthedocs.io/en/latest/configuration.html
#
myst_heading_anchors = 2

myst_enable_extensions = [
    # available extensions: https://myst-parser.readthedocs.io/en/latest/syntax/optional.html
    "attrs_inline",
    "colon_fence",
    "deflist",
    "dollarmath",
    "fieldlist",
]

# -- Options for linkcheck builder -------------------------------------------
# ref: https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-the-linkcheck-builder
#
linkcheck_ignore = [
    r"(.*)github\.com(.*)#",  # javascript based anchors
    r"(.*)/#%21(.*)/(.*)",  # /#!forum/jupyter - encoded anchor edge case
    r"https://github.com/[^/]*$",  # too many github usernames / searches in changelog
    "https://github.com/jupyterhub/the-littlest-jupyterhub/pull/",  # too many PRs in changelog
    "https://github.com/jupyterhub/the-littlest-jupyterhub/compare/",  # too many comparisons in changelog
]
linkcheck_anchors_ignore = [
    "/#!",
    "/#%21",
]


# -- Options for the opengraph extension -------------------------------------
# ref: https://github.com/wpilibsuite/sphinxext-opengraph#options
#
# ogp_site_url is set automatically by RTD
ogp_image = "_static/logo.png"
ogp_use_first_image = True


# -- Options for the rediraffe extension -------------------------------------
# ref: https://github.com/wpilibsuite/sphinxext-rediraffe#readme
#
# This extensions help us relocated content without breaking links. If a
# document is moved internally, we should configure a redirect like below.
#
rediraffe_branch = "main"
rediraffe_redirects = {
    # "old-file": "new-folder/new-file-name",
    "howto/env/user-environment": "howto/user-env/user-environment",
    "howto/env/notebook-interfaces": "howto/user-env/notebook-interfaces",
    "howto/env/server-resources": "howto/user-env/server-resources",
}
