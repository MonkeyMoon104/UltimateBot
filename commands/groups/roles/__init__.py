from utils.library.libs import *
from discord import app_commands
from .role_all import role_all
from .role_bot import role_bot
from .role_add import role_add
from .role_remove import role_remove
from .role_in import role_in

class RoleGroup(app_commands.Group):
    def __init__(self):
        super().__init__(name="role", description="Gestione ruoli nel server")
        self.add_command(role_all)
        self.add_command(role_bot)
        self.add_command(role_add)
        self.add_command(role_remove)
        self.add_command(role_in)

acromrole = RoleGroup()
