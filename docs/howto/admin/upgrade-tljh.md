(howto-admin-upgrade-tljh)=

# Upgrade TLJH

A TLJH installation is supposed to be upgradable to get updates to JupyterHub
itself and its dependencies in the [hub environment](hub-environment). For
details on what is done during an upgrade, see
[](topic-installer-upgrade-actions).

## Step 1: Read the changelog

Before making an upgrade, please read the [](changelog) to become aware about
breaking changes. If there are breaking changes, you may need to update your
configuration files or take other actions as well as part of the upgrade.

Adjusting to the breaking changes isn't part of this documentation, please rely
on the TLJH changelog and the changelogs of related projects linked to from the
TLJH changelog.

## Step 2: Consider making a backup

Before making an upgrade, consider if you want to first make a backup in some
way. While upgrades between TLJH versions are tested with automation, there are
no guarantees.

This project does't yet provide documentation on how to make backups, but if
TLJH is installed on a virtual machine in a cloud, a good option is to try
create a snapshot of the associated disk. If this isn't an option, you could
consider making a backup of the files in `/opt/tljh` that contain most but not
all things during an upgrade, or perhaps only the JupyterHub database with
information about its users in `/opt/tljh/state` together with some other
details.

## Step 3: Make the upgrade

To initialize the upgrade, do the following from a terminal on the machine where
TLJH is installed.

```shell
# IMPORTANT: This should NOT be run from a JupyterHub started user server, but
#            should only run from a standalone terminal session in the machine
#            where TLJH has been installed.
#
curl -L https://tljh.jupyter.org/bootstrap.py \
  | sudo python3 - \
    --version=latest
```

You can also upgrade to specific version by changing `--version=latest` to
`--version=1.0.0` or similar. There is no need to specify admin users etc again.

## Step 4: Verify function

After having made an upgrade its always good to verify that the JupyterHub
installation still works as expected. You may want to try logging out, logging
in, and starting a new server for example.

If you have issues consider the [](troubleshooting) documentation. If you need
help you can ask questions in [Jupyter forum], and if you think there is a bug
or documentation improvement that should be made you can open an issue or pull
request in the [TLJH GitHub project].

[jupyter forum]: https://discourse.jupyter.org/c/jupyterhub/tljh
[tljh github project]: https://github.com/jupyterhub/the-littlest-jupyterhub
