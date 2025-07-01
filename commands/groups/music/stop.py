import discord
from discord import app_commands
from utils.func_utils import SONG_QUEUES

class StopCommand(app_commands.Command):
    def __init__(self):
        super().__init__(
            name="stop",
            description="Ferma la musica",
            callback=self.callback
        )

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        voice_client = interaction.guild.voice_client

        if not voice_client or not voice_client.is_connected():
            return await interaction.followup.send("I'm not connected to any voice channel.", ephemeral=True)

        guild_id_str = str(interaction.guild_id)
        if guild_id_str in SONG_QUEUES:
            SONG_QUEUES[guild_id_str].clear()

        if voice_client.is_playing() or voice_client.is_paused():
            voice_client.stop()

        await voice_client.disconnect()

        await interaction.followup.send("Stopped playback and disconnected!", ephemeral=True)
