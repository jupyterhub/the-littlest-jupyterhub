import os

source_suffix = [".rst"]

project = "The Littlest JupyterHub"
copyright = "2018, JupyterHub Team"
author = "JupyterHub Team"

# The short X.Y version
version = ""
# The full version, including alpha/beta/rc tags
release = "v0.1"

# Enable MathJax for Math
extensions = [
    "sphinx.ext.mathjax",
    "sphinx.ext.intersphinx",
    "sphinx_copybutton",
]

# The root toctree document.
root_doc = master_doc = "index"

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path .
exclude_patterns = [
    "_build",
    "Thumbs.db",
    ".DS_Store",
    "install/custom.rst",
]

intersphinx_mapping = {
    "sphinx": ("http://www.sphinx-doc.org/en/master/", None),
}

intersphinx_cache_limit = 90  # days

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = "sphinx"

html_theme = "pydata_sphinx_theme"

html_logo = "images/logo/logo.png"
html_favicon = "images/logo/favicon.ico"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
# Do this only if _static exists, otherwise this will error
here = os.path.dirname(os.path.abspath(__file__))
if os.path.exists(os.path.join(here, "_static")):
    html_static_path = ["_static"]
