import discord
from discord import app_commands

class SkipCommand(app_commands.Command):
    def __init__(self):
        super().__init__(
            name="skip",
            description="skippa la musica",
            callback=self.callback
        )

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        if interaction.guild.voice_client and (interaction.guild.voice_client.is_playing() or interaction.guild.voice_client.is_paused()):
            interaction.guild.voice_client.stop()
            await interaction.followup.send("Skipped the current song.", ephemeral=True)
        else:
            await interaction.followup.send("Not playing anything to skip.", ephemeral=True)
