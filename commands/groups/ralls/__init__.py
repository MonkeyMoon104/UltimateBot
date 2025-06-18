from discord import app_commands
from .rall_all import rall_all
from .rall_bot import rall_bot
from .rall_in import rall_in

class RallGroup(app_commands.Group):
    def __init__(self):
        super().__init__(name="rall", description="Rimozione ruoli dal server")
        self.add_command(rall_all)
        self.add_command(rall_bot)
        self.add_command(rall_in)

acromrall = RallGroup()
