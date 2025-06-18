import discord
from discord import app_commands
from data.config import *

@app_commands.context_menu(name="Joined at")
async def get_joined_date(interaction: discord.Interaction, member: discord.Member):

    embed_join = discord.Embed(title=f"Date join for {member.name}", color=discord.Color.yellow())
    embed_join.set_thumbnail(url=ICONACROM)
    embed_join.set_footer(icon_url=ICONACROM, text="Powered by Acrom")
    embed_join.add_field(name="Joined at", value=discord.utils.format_dt(member.joined_at))

    await interaction.response.send_message(embed=embed_join, ephemeral=True)

context_menu_command = get_joined_date