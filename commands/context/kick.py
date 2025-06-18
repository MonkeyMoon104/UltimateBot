import discord
from discord import app_commands
from data.config import *

@app_commands.context_menu(name="Kick")
async def kick_command(interaction: discord.Interaction, member: discord.Member):
    if interaction.user.guild_permissions.administrator or interaction.user.guild_permissions.ban_members or interaction.user.guild_permissions.kick_members:

        await member.kick(reason="Context Command")
            
        embedkick = discord.Embed(title="New Kick ", color=discord.Color.yellow())
        embedkick.add_field(name="Utente Kickato ", value=member.mention, inline=False)
        embedkick.add_field(name="Kickato da ", value=interaction.user.mention, inline=False)
        embedkick.add_field(name="Motivo ", value="Context Command", inline=False)
        embedkick.set_footer(icon_url=ICONACROM, text="Powered by Acrom")
        embedkick.set_thumbnail(url=ICONACROM)
            
        await interaction.response.send_message(embed=embedkick)
    else:
        embedbannoperm = discord.Embed(title="No perms ", description="Non hai il permesso (administrator or ban_members or kick_members) per eseguire questo comando", color=discord.Color.red())
        embedbannoperm.set_footer(icon_url=ICONACROM, text="Powered by Acrom")
        embedbannoperm.set_thumbnail(url=ICONACROM)

        await interaction.response.send_message(embed=embedbannoperm, ephemeral=True)

context_menu_command = kick_command