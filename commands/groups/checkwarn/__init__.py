from discord import app_commands
from .check_warn import CheckWarnCommand
from .check_warnings import CheckWarningsCommand

class CheckWarnGroup(app_commands.Group):
    def __init__(self):
        super().__init__(name="checkwarn", description="Controllo warn staff")
        self.add_command(CheckWarnCommand())
        self.add_command(CheckWarningsCommand())

checkwarn = CheckWarnGroup()
