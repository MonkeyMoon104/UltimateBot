from utils.library.libs import *

class ChannelsTicketLink(discord.ui.View):
    def __init__(self, server_id: str, channel_id: str):
        super().__init__()
        self.server_id = server_id
        self.channel_id = channel_id
        self.add_item(discord.ui.Button(label="Il Tuo Ticket", url=f"https://discord.com/channels/{self.server_id}/{self.channel_id}", emoji="🔗"))