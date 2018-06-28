from recommonmark.parser import CommonMarkParser
from recommonmark.transform import AutoStructify

# Support markdown too
source_suffix = ['.rst']

project = 'The Littlest JupyterHub'
copyright = '2018, JupyterHub Team'
author = 'JupyterHub Team'

# The short X.Y version
version = ''
# The full version, including alpha/beta/rc tags
release = 'v0.1'

# The master toctree document.
master_doc = 'index'

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path .
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

html_theme = 'alabaster'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']
