from discord import app_commands
from .warn_staff import WarnStaffCommand
from .remove_all_warn import RemoveAllWarnCommand

class WarnGroup(app_commands.Group):
    def __init__(self):
        super().__init__(name="warn", description="Gestione warn staff")
        self.add_command(WarnStaffCommand())
        self.add_command(RemoveAllWarnCommand())

warnstaff = WarnGroup()
