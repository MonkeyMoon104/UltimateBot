import discord

class BannerViewLink(discord.ui.View):
    def __init__(self, banner_link: str):
        super().__init__()
        self.banner_link = banner_link
        self.add_item(discord.ui.Button(label="Banner Url", url=self.banner_link))