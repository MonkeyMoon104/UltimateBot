from discord import app_commands
from .setup import SetupCommand
from .purge import PurgeCommand
from .rename import RenameCommandGroup
from .add import AddCommand


class TicketAcrom(app_commands.Group):
    def __init__(self):
        super().__init__(name="ticket", description="Ticket commands")
        self.add_command(SetupCommand())
        self.add_command(PurgeCommand())
        self.add_command(RenameCommandGroup().rename)
        self.add_command(AddCommand())


ticketacrom = TicketAcrom()
