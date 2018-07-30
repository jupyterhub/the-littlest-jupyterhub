# Support markdown too
source_suffix = ['.rst']

project = 'The Littlest JupyterHub'
copyright = '2018, JupyterHub Team'
author = 'JupyterHub Team'

# The short X.Y version
version = ''
# The full version, including alpha/beta/rc tags
release = 'v0.1'

# Add custom CSS/Javascript
def setup(app):
    app.add_javascript("custom.js")
    app.add_stylesheet("custom.css")
    app.add_javascript("https://cdn.jsdelivr.net/npm/clipboard@1/dist/clipboard.min.js")

# Enable MathJax for Math
extensions = ['sphinx.ext.mathjax']

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

# Configure the sidebar to be how we want it to be
# We don't have 'navigation' here, since it is very cluttered
# and seems to be hard to control.
html_sidebars = {
    '**': [
        'about.html',
        'relations.html',
        'searchbox.html',
        'donate.html',
    ]
}
# Custom Alabaster theme options
html_theme_options = {
    'description': """
    A simple JupyterHub distribution for 1-100 users
    <br /> <br />
    <strong>Documentation confusing?</strong> <a href="https://github.com/jupyterhub/the-littlest-jupyterhub/issues">File an issue!</a>
    """,
    'github_user': 'jupyterhub',
    'github_repo': 'the-littlest-jupyterhub',
    'github_button': True,
    'github_banner': True,
}
