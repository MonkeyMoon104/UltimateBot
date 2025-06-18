import discord
from discord import app_commands
from data.config import ICONACROM, HEADSTAFF_ROLE_ID


class PurgeCommand(app_commands.Command):
    def __init__(self):
        super().__init__(name="purge", description="Delete all tickets in the server", callback=self.callback)

    async def callback(self, interaction: discord.Interaction):
        if HEADSTAFF_ROLE_ID in [role.id for role in interaction.user.roles]:
            for channel in interaction.guild.channels:
                if isinstance(channel, discord.TextChannel) and channel.topic and 'Ticket open by' in channel.topic:
                    try:
                        await channel.delete()
                    except discord.Forbidden:
                        print(f"Insufficient permissions to delete channel {channel.name}.")
                    except discord.HTTPException as e:
                        print(f"Error deleting channel {channel.name}: {e}")
            await interaction.response.send_message("Ticket channels purged successfully", ephemeral=True)
        else:
            embedmessagenoperm = discord.Embed(
                title="No perms",
                description="You don't have the (administrator) permission to execute this command",
                color=discord.Color.red()
            )
            embedmessagenoperm.set_footer(icon_url=ICONACROM, text="Powered by Acrom")
            embedmessagenoperm.set_thumbnail(url=ICONACROM)
            await interaction.response.send_message(embed=embedmessagenoperm, ephemeral=True)
