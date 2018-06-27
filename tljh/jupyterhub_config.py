"""
JupyterHub config for the littlest jupyterhub.
"""
from escapism import escape
import os
from systemdspawner import SystemdSpawner
from tljh import user

INSTALL_PREFIX = os.environ.get('TLJH_INSTALL_PREFIX')
USER_ENV_PREFIX = os.path.join(INSTALL_PREFIX, 'user')

class CustomSpawner(SystemdSpawner):
    def start(self):
        """
        Perform system user activities before starting server
        """
        # FIXME: Move this elsewhere? Into the Authenticator?
        user.ensure_user(self.user.name)
        user.ensure_user_group(self.user.name, 'jupyterhub-users')
        if self.user.admin:
            user.ensure_user_group(self.user.name, 'jupyterhub-admins')
        else:
            user.remove_user_group(self.user.name, 'jupyterhub-admins')
        return super().start()


c.JupyterHub.spawner_class = CustomSpawner
c.JupyterHub.authenticator_class = 'dummyauthenticator.DummyAuthenticator'

c.SystemdSpawner.extra_paths = [os.path.join(USER_ENV_PREFIX, 'bin')]
c.SystemdSpawner.use_sudo = True
