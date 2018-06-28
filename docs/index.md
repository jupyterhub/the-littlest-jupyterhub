# The Littlest JupyterHub

A simple [JupyterHub](https://github.com/jupyterhub/jupyterhub) distribution for
a small (0-50) number of users on a single server.

## Quick Start

On a fresh Ubuntu 18.04 server, you can install The Littlest JupyterHub with:

```bash
curl https://raw.githubusercontent.com/yuvipanda/the-littlest-jupyterhub/master/installer/install.bash | sudo bash -
```

This takes 2-5 minutes to run. When completed, you can access your new JupyterHub
at the public IP of your server!

If this installation method (`curl <arbitrary-url> | sudo bash -`)
makes you nervous, check out the [other installation methods](install.md) we support!

## Table of Contents

- [Server requirements](requirements.md)
- [Installation](install.md)
- [Administrative Access](admin.md)
