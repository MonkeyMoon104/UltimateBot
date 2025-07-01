from utils.library.libs import *

class ProfileViewLinks(discord.ui.View):
    def __init__(self):
        super().__init__()

    def add_link(self, label: str, url: str):
        self.add_item(discord.ui.Button(label=label, url=url))