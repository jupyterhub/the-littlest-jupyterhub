from setuptools import setup, find_packages

setup(
    name='the-littlest-jupyterhub',
    version='0.1',
    description='A small JupyterHub distribution',
    url='https://github.com/yuvipanda/the-littlest-jupyterhub',
    author='Yuvi Panda',
    author_email='yuvipanda@gmail.com',
    license='3 Clause BSD',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'pyyaml==3.*',
        'ruamel.yaml==0.15.*'
    ]
)
