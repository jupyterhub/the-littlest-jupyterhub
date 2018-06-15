import os

c.JupyterHub.spawner_class = 'systemdspawner.SystemdSpawner'

c.JupyterHub.authenticator_class = 'dummyauthenticator.DummyAuthenticator'

# FIXME: ensure user conda environment is installed & has necessary packages.
here = os.getcwd()
c.SystemdSpawner.extra_paths = [os.path.join(here, 'user-environment/bin')]