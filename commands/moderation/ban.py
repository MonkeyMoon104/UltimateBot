from utils.library.libs import *
from data.config import ICONACROM
from discord import app_commands

@app_commands.command(name="ban", description="Banna un utente")
@app_commands.describe(member="Utente da bannare", reason="Motivo del ban")
async def ban(interaction: discord.Interaction, member: discord.Member, *, reason: str):
    if interaction.user.guild_permissions.ban_members or interaction.user.guild_permissions.administrator:
        await member.ban(reason=reason)
        embed = discord.Embed(title="New Ban", color=discord.Color.yellow())
        embed.add_field(name="Utente Bannato", value=member.mention, inline=False)
        embed.add_field(name="Bannato da", value=interaction.user.mention, inline=False)
        embed.add_field(name="Motivo", value=reason, inline=False)
    else:
        embed = discord.Embed(title="No perms", description="Non hai il permesso (administrator o ban_members)", color=discord.Color.red())

    embed.set_footer(icon_url=ICONACROM, text="Powered by Acrom")
    embed.set_thumbnail(url=ICONACROM)
    await interaction.response.send_message(embed=embed, ephemeral=not interaction.user.guild_permissions.ban_members)

command = ban

