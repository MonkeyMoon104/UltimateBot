from utils.library.libs import *

class AvatarViewLink(discord.ui.View):
    def __init__(self, avatar_link: str):
        super().__init__()
        self.avatar_link = avatar_link
        self.add_item(discord.ui.Button(label="Avatar Url", url=self.avatar_link))