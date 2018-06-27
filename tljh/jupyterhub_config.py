"""
JupyterHub config for the littlest jupyterhub.
"""
import os
from systemdspawner import SystemdSpawner
from tljh import user, configurer

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

c.ConfigurableHTTPProxy.should_start = False

c.SystemdSpawner.extra_paths = [os.path.join(USER_ENV_PREFIX, 'bin')]
c.SystemdSpawner.use_sudo = True

configurer.apply_yaml_config('/etc/jupyterhub/jupyterhub.yaml', c)
