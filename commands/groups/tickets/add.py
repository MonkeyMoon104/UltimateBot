from utils.library.libs import *
from data.config import ICONACROM, HEADSTAFF_ROLE_ID
from discord import app_commands

class AddCommand(app_commands.Command):
    def __init__(self):
        super().__init__(
            name="add",
            description="Add a member or role to a ticket",
            callback=self.callback,
        )

    async def callback(self, interaction: discord.Interaction, target: typing.Union[discord.Member, discord.Role], channel: discord.TextChannel):
        if HEADSTAFF_ROLE_ID in [role.id for role in interaction.user.roles]:
            if channel.topic and 'Ticket open by' in channel.topic:
                try:
                    await channel.set_permissions(target, send_messages=True, read_message_history=True, view_channel=True)
                    await interaction.response.send_message(f"{target.mention} has been added to {channel.mention}", ephemeral=True)
                except discord.Forbidden:
                    await interaction.response.send_message(f"Insufficient permissions to add {target.mention} to {channel.mention}", ephemeral=True)
                except discord.HTTPException as e:
                    await interaction.response.send_message(f"Error adding {target.mention} to {channel.mention}: {e}", ephemeral=True)
            else:
                await interaction.response.send_message(f"{channel.mention} is not a ticket", ephemeral=True)
        else:
            embedmessagenoperm = discord.Embed(
                title="No perms",
                description="You don't have the (administrator) permission to execute this command",
                color=discord.Color.red()
            )
            embedmessagenoperm.set_footer(icon_url=ICONACROM, text="Powered by Acrom")
            embedmessagenoperm.set_thumbnail(url=ICONACROM)
            await interaction.response.send_message(embed=embedmessagenoperm, ephemeral=True)
