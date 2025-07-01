from utils.library.libs import *
from data.config import ICONACROM
from discord import app_commands

@app_commands.command(name="untimeout", description="Rimuovi il timeout ad un utente")
@app_commands.describe(member="Utente a cui rimuovere il timeout", reason="Motivo")
async def untimeout(interaction: discord.Interaction, member: discord.Member, *, reason: str):
    if not (interaction.user.guild_permissions.moderate_members or interaction.user.guild_permissions.administrator):
        embed = discord.Embed(title="No perms", description="Non hai il permesso (administrator o moderate_members)", color=discord.Color.red())
        embed.set_footer(icon_url=ICONACROM, text="Powered by Acrom")
        embed.set_thumbnail(url=ICONACROM)
        return await interaction.response.send_message(embed=embed, ephemeral=True)

    try:
        await member.timeout(Utils.utcnow() + timedelta(seconds=0), reason=reason)
    except:
        return await interaction.response.send_message(f"Non ho il permesso di togliere il timeout a {member}", ephemeral=True)

    embed = discord.Embed(title="New untimeout", color=discord.Color.yellow())
    embed.add_field(name="Utente", value=member.mention, inline=False)
    embed.add_field(name="Rimosso da", value=interaction.user.mention, inline=False)
    embed.add_field(name="Motivo", value=reason, inline=False)
    embed.set_footer(icon_url=ICONACROM, text="Powered by Acrom")
    embed.set_thumbnail(url=ICONACROM)
    await interaction.response.send_message(embed=embed)

command = untimeout