import discord
from discord import app_commands
from data.config import *
from utils.classes.views.avatar_view_link import AvatarViewLink

@app_commands.context_menu(name="See Avatar")
async def see_avatar(interaction: discord.Interaction, member: discord.Member):
    url_avatar = member.avatar.url
    embed_avatar = discord.Embed(title=f"Avatar of {member.name}", color=discord.Color.yellow())
    embed_avatar.set_thumbnail(url=ICONACROM)
    embed_avatar.set_footer(icon_url=ICONACROM, text="Powered by Acrom")
    embed_avatar.set_image(url=url_avatar)

    await interaction.response.send_message(embed=embed_avatar, view=AvatarViewLink(url_avatar), ephemeral=True)

context_menu_command = see_avatar
