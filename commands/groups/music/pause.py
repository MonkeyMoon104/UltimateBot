import discord
from discord import app_commands

class PauseCommand(app_commands.Command):
    def __init__(self):
        super().__init__(
            name="pause",
            description="Metti in pausa la musica",
            callback=self.callback
        )

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        voice_client = interaction.guild.voice_client

        if voice_client is None:
            return await interaction.followup.send("I'm not in a voice channel.", ephemeral=True)

        if not voice_client.is_playing():
            return await interaction.followup.send("Nothing is currently playing.", ephemeral=True)
        
        voice_client.pause()
        await interaction.followup.send("Playback paused!", ephemeral=True)
