from utils.library.libs import *
from utils.func_utils import channel_autocomplete
from data.config import ICONACROM, HEADSTAFF_ROLE_ID
from discord import app_commands


class RenameCommandGroup(app_commands.Group):
    def __init__(self):
        super().__init__(name="ticket", description="Ticket commands")

    @app_commands.command(name="rename", description="Rename a ticket in a server")
    @app_commands.autocomplete(channel=channel_autocomplete)
    async def rename(
        self,
        interaction: discord.Interaction,
        channel: str,
        new_name: str,
    ):
        if HEADSTAFF_ROLE_ID not in [role.id for role in interaction.user.roles]:
            embedmessagenoperm = discord.Embed(
                title="No perms",
                description="You don't have the (administrator) permission to execute this command",
                color=discord.Color.red(),
            )
            embedmessagenoperm.set_footer(icon_url=ICONACROM, text="Powered by Acrom")
            embedmessagenoperm.set_thumbnail(url=ICONACROM)
            await interaction.response.send_message(embed=embedmessagenoperm, ephemeral=True)
            return

        selected_channel = discord.utils.get(interaction.guild.text_channels, name=channel)
        if not selected_channel:
            embed_error = discord.Embed(
                title="Error",
                description=f"Il canale '{channel}' non è un valido ticket channel",
                color=discord.Color.red(),
            )
            embed_error.set_footer(icon_url=ICONACROM, text="Powered by Acrom")
            await interaction.response.send_message(embed=embed_error, ephemeral=True)
            return

        try:
            await selected_channel.edit(name=new_name)
            embed_success = discord.Embed(
                title="Success",
                description=f"Rinominazione del canale '{new_name}' eseguita con successo.",
                color=discord.Color.green(),
            )
            embed_success.set_footer(icon_url=ICONACROM, text="Powered by Acrom")
            await interaction.response.send_message(embed=embed_success)
        except Exception as e:
            embed_error = discord.Embed(
                title="Error",
                description=f"An error occurred while renaming the channel: {e}",
                color=discord.Color.red(),
            )
            embed_error.set_footer(icon_url=ICONACROM, text="Powered by Acrom")
            await interaction.response.send_message(embed=embed_error, ephemeral=True)