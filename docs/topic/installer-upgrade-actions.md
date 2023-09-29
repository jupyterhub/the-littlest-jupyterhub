(topic-installer-upgrade-actions)=

# What is done during an upgrade of TLJH?

Once TLJH has been installed, it should be possible to upgrade the installation.
This documentation is meant to capture the changes made during an upgrade.

```{versionchanged} 1.0.0
Ensuring upgrades work has only been done since 1.0.0 upgrading from version
0.2.0.
```

## Changes to the system environment

The [system environment](system-environment) is not meant to be influenced
unless explicitly mentioned in the changelog, typically only during major
version upgrades.

## Changes to the hub environment

The [hub environment](hub-environment) gets several packages upgraded based on
version ranges specified in [tljh/requirements-hub-env.txt].

## Changes to the user environment

The [user environment](user-environment) gets is `jupyterhub` package upgraded,
but no other packages gets upgraded unless explicitly mentioned in the
changelog, typically only during major version upgrades.

[tljh/requirements-hub-env.txt]: https://github.com/jupyterhub/the-littlest-jupyterhub/blob/HEAD/tljh/requirements-hub-env.txt
