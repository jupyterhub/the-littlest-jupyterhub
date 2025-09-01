# The Littlest JupyterHub

[![Documentation build status](https://img.shields.io/readthedocs/the-littlest-jupyterhub?logo=read-the-docs)](https://tljh.jupyter.org/en/latest/?badge=latest)
[![GitHub Workflow Status - Test](https://img.shields.io/github/actions/workflow/status/jupyterhub/the-littlest-jupyterhub/integration-test.yaml?logo=github&label=tests)](https://github.com/jupyterhub/the-littlest-jupyterhub/actions)
[![Test coverage of code](https://codecov.io/gh/jupyterhub/the-littlest-jupyterhub/branch/main/graph/badge.svg)](https://codecov.io/gh/jupyterhub/the-littlest-jupyterhub)
[![GitHub](https://img.shields.io/badge/issue_tracking-github-blue?logo=github)](https://github.com/jupyterhub/the-littlest-jupyterhub/issues)
[![Discourse](https://img.shields.io/badge/help_forum-discourse-blue?logo=discourse)](https://discourse.jupyter.org/c/jupyterhub/tljh)
[![Gitter](https://img.shields.io/badge/social_chat-gitter-blue?logo=gitter)](https://gitter.im/jupyterhub/jupyterhub)
[![Contribute](https://img.shields.io/badge/I_want_to_contribute!-grey?logo=jupyter)](https://tljh.jupyter.org/en/latest/contributing/index.html)

**The Littlest JupyterHub** (TLJH) distribution helps you provide Jupyter Notebooks
to 1-100 users on a single server.

The primary audience are people who do not consider themselves 'system administrators'
but would like to provide hosted Jupyter Notebooks for their students or users.
All users are provided with the same environment, and administrators
can easily install libraries into this environment without any specialized knowledge.

See the [latest documentation](https://the-littlest-jupyterhub.readthedocs.io)
for more information on using The Littlest JupyterHub.

For support questions please search or post to [our forum](https://discourse.jupyter.org/c/jupyterhub/).

See the [contributing guide](https://the-littlest-jupyterhub.readthedocs.io/en/latest/contributing/index.html)
for information on the different ways of contributing to The Littlest JupyterHub.

See [this blog post](http://words.yuvi.in/post/the-littlest-jupyterhub/) for
more information.

## Installation

The Littlest JupyterHub (TLJH) can run on any server that is running at least
**Ubuntu 22.04**. Earlier versions of Ubuntu are not supported.
We have several tutorials to get you started.

- Tutorials to create a new server from scratch on a cloud provider & run TLJH
  on it. These are **recommended** if you do not have much experience setting up
  servers.
  - [Digital Ocean](https://the-littlest-jupyterhub.readthedocs.io/en/latest/install/digitalocean.html)
  - [OVH](https://the-littlest-jupyterhub.readthedocs.io/en/latest/install/ovh.html)
  - [Google Cloud](https://the-littlest-jupyterhub.readthedocs.io/en/latest/install/google.html)
  - [Jetstream](https://the-littlest-jupyterhub.readthedocs.io/en/latest/install/jetstream.html)
  - [Amazon Web Services](https://the-littlest-jupyterhub.readthedocs.io/en/latest/install/amazon.html)
  - [Microsoft Azure](https://the-littlest-jupyterhub.readthedocs.io/en/latest/install/azure.html)
  - ... your favorite provider here, if you can contribute!

- [Tutorial to install TLJH on an already running server you have root access to](https://the-littlest-jupyterhub.readthedocs.io/en/latest/install/custom-server.html).
  You should use this if your cloud provider does not already have a direct tutorial,
  or if you have experience setting up servers.

## Documentation

Our latest documentation is at: https://the-littlest-jupyterhub.readthedocs.io

We place a high importance on consistency, readability and completeness of
documentation. If a feature is not documented, it does not exist. If a behavior
is not documented, it is a bug! We try to treat our documentation like we treat
our code: we aim to improve it as often as possible.

If something is confusing to you in the documentation, it is a bug. We would be
happy if you could [file an issue](https://github.com/jupyterhub/the-littlest-jupyterhub/issues) about it - or
even better, [contribute a documentation fix](http://the-littlest-jupyterhub.readthedocs.io/en/latest/contributing/docs.html)!
