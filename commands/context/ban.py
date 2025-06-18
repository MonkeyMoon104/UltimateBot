import discord
from discord import app_commands
from data.config import *

@app_commands.context_menu(name="Ban")
async def ban_command(interaction: discord.Interaction, member: discord.Member):
    if interaction.user.guild_permissions.administrator or interaction.user.guild_permissions.ban_members:

        await member.ban(reason="Context Command")
            
        embedban = discord.Embed(title="New Ban ", color=discord.Color.yellow())
        embedban.add_field(name="Utente Bannato ", value=member.mention, inline=False)
        embedban.add_field(name="Bannato da ", value=interaction.user.mention, inline=False)
        embedban.add_field(name="Motivo ", value="Context Command", inline=False)
        embedban.set_footer(icon_url=ICONACROM, text="Powered by Acrom")
        embedban.set_thumbnail(url=ICONACROM)
            
        await interaction.response.send_message(embed=embedban)
    else:
        embedbannoperm = discord.Embed(title="No perms ", description="Non hai il permesso (administrator or ban_members) per eseguire questo comando", color=discord.Color.red())
        embedbannoperm.set_footer(icon_url=ICONACROM, text="Powered by Acrom")
        embedbannoperm.set_thumbnail(url=ICONACROM)

        await interaction.response.send_message(embed=embedbannoperm, ephemeral=True)

context_menu_command = ban_command