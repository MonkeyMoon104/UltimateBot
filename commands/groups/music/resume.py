import discord
from discord import app_commands

class ResumeCommand(app_commands.Command):
    def __init__(self):
        super().__init__(
            name="resume",
            description="Riprendi la musica",
            callback=self.callback
        )

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        voice_client = interaction.guild.voice_client

        if voice_client is None:
            return await interaction.followup.send("I'm not in a voice channel.", ephemeral=True)

        if not voice_client.is_paused():
            return await interaction.followup.send("I’m not paused right now.", ephemeral=True)
        
        voice_client.resume()
        await interaction.followup.send("Playback resumed!", ephemeral=True)
