from setuptools import find_packages, setup

setup(
    name="the-littlest-jupyterhub",
    version="2.0.0.dev",
    description="A small JupyterHub distribution",
    url="https://github.com/jupyterhub/the-littlest-jupyterhub",
    author="Jupyter Development Team",
    author_email="jupyter@googlegroups.com",
    license="3 Clause BSD",
    packages=find_packages(),
    include_package_data=True,
    python_requires=">=3.9",
    install_requires=[
        "ruamel.yaml==0.18.*",
        "jinja2",
        "pluggy==1.*",
        "backoff",
        "filelock",
        "requests",
        "bcrypt",
        "jupyterhub-traefik-proxy==2.*",
    ],
    entry_points={
        "console_scripts": [
            "tljh-config = tljh.config:main",
        ]
    },
)
