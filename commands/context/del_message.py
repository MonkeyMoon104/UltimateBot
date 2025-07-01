from utils.library.libs import *
from data.config import *
from discord import app_commands

@app_commands.context_menu(name="Delete Message")
async def delete_message(interaction: discord.Interaction, message: discord.Message):
    if interaction.user.guild_permissions.administrator or interaction.user.guild_permissions.manage_messages:
        await message.delete()
        await interaction.response.send_message("Message deleted!", ephemeral=True)

    else:
        embedmessagenoperm = discord.Embed(title="No perms ", description="Non hai il permesso (administrator or manage_messages) per eseguire questo comando", color=discord.Color.red())
        embedmessagenoperm.set_footer(icon_url=ICONACROM, text="Powered by Acrom")
        embedmessagenoperm.set_thumbnail(url=ICONACROM)

        await interaction.response.send_message(embed=embedmessagenoperm, ephemeral=True)

context_menu_command = delete_message