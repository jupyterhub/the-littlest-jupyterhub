# The Littlest JupyterHub

A simple [JupyterHub](https://github.com/jupyterhub/jupyterhub) distribution for
a small (0-100) number of users on a single server. We recommend reading
[](/topic/whentouse) to determine if this is the right tool for you.

## Installation

The Littlest JupyterHub (TLJH) can run on any server that is running **Debian 11** or **Ubuntu 20.04** or **22.04** on an amd64 or arm64 CPU architecture.
We aim to support 'stable' and Long-Term Support (LTS) versions.
Newer versions are likely to work with little or no adjustment, but these are not officially supported or tested.
Earlier versions of Ubuntu and Debian are not supported, nor are other Linux distributions.
We have a bunch of tutorials to get you started.

- Tutorials to create a new server from scratch on a cloud provider & run TLJH
  on it. These are **recommended** if you do not have much experience setting up
  servers.

  ```{toctree}
  :maxdepth: 2
  :titlesonly: true

  install/index
  ```

Once you are ready to run your server for real,
it's a good idea to proceed directly to {doc}`howto/admin/https`.

## How-To Guides

How-To guides answer the question 'How do I...?' for a lot of topics.

```{toctree}
:maxdepth: 2

howto/index
```

## Topic Guides

Topic guides provide in-depth explanations of specific topics.

```{toctree}
:maxdepth: 2
:titlesonly: true

topic/index
```

## Reference

The reference documentation is meant to provide narrowly scoped technical
descriptions that other documentation can link to for details.

```{toctree}
:maxdepth: 2
:titlesonly: true

reference/index
```

## Troubleshooting

In time, all systems have issues that need to be debugged. Troubleshooting
guides help you find what is broken & hopefully fix it.

```{toctree}
:maxdepth: 2
:titlesonly: true

troubleshooting/index
```

## Contributing

We want you to contribute to TLJH in the ways that are most useful
and exciting to you. This section contains documentation helpful
to people contributing in various ways.

```{toctree}
:maxdepth: 2
:titlesonly: true

contributing/index
```
