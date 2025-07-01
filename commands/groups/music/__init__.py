from discord import app_commands
from .play import PlayCommand
from .stop import StopCommand
from .skip import SkipCommand
from .pause import PauseCommand
from .resume import ResumeCommand

class MusicGroup(app_commands.Group):
    def __init__(self):
        super().__init__(name="music", description="Gestisci le canzoni")
        self.add_command(PlayCommand())
        self.add_command(StopCommand())
        self.add_command(SkipCommand())
        self.add_command(PauseCommand())
        self.add_command(ResumeCommand())

music = MusicGroup()