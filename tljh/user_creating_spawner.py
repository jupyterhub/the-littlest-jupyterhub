from tljh.normalize import generate_system_username
from tljh import user
from systemdspawner import SystemdSpawner
from traitlets import Dict, Unicode, List
from jupyterhub_configurator.mixins import ConfiguratorSpawnerMixin

class UserCreatingSpawner(ConfiguratorSpawnerMixin, SystemdSpawner):
    """
    SystemdSpawner with user creation on spawn.

    FIXME: Remove this somehow?
    """
    user_groups = Dict(key_trait=Unicode(), value_trait=List(Unicode()), config=True)

    def start(self):
        """
        Perform system user activities before starting server
        """
        # FIXME: Move this elsewhere? Into the Authenticator?
        system_username = generate_system_username('jupyter-' + self.user.name)

        # FIXME: This is a hack. Allow setting username directly instead
        self.username_template = system_username
        user.ensure_user(system_username)
        user.ensure_user_group(system_username, 'jupyterhub-users')
        if self.user.admin:
            user.ensure_user_group(system_username, 'jupyterhub-admins')
        else:
            user.remove_user_group(system_username, 'jupyterhub-admins')
        if self.user_groups:
            for group, users in self.user_groups.items():
                if self.user.name in users:
                    user.ensure_user_group(system_username, group)
        return super().start()

