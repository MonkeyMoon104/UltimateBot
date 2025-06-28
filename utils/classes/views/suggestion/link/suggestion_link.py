import discord

class SuggestionLink(discord.ui.View):
    def __init__(self, url_link: str):
        super().__init__()
        self.url_link = url_link
        self.add_item(discord.ui.Button(label="Suggestion", url=url_link, emoji="💡"))