from utils.library.libs import *
from data.config import ICONACROM
from discord import app_commands

@app_commands.command(name="timeout", description="Metti in timeout un utente")
@app_commands.describe(member="Utente da mettere in timeout", time="Durata timeout (es. 2m, 1h, 1d)", reason="Motivo del timeout")
async def timeout(interaction: discord.Interaction, member: discord.Member, *, time: str, reason: str):
    if not (interaction.user.guild_permissions.moderate_members or interaction.user.guild_permissions.administrator):
        embed = discord.Embed(title="No perms", description="Non hai il permesso (administrator o moderate_members)", color=discord.Color.red())
        embed.set_footer(icon_url=ICONACROM, text="Powered by Acrom")
        embed.set_thumbnail(url=ICONACROM)
        return await interaction.response.send_message(embed=embed, ephemeral=True)

    try:
        seconds = parse_timespan(time)
    except InvalidTimespan:
        return await interaction.response.send_message(f"{time} non è un'opzione valida (es. 2s, 5m, 3d)", ephemeral=True)

    try:
        await member.timeout(Utils.utcnow() + timedelta(seconds=seconds), reason=reason)
    except:
        return await interaction.response.send_message(f"Non ho il permesso di mettere in timeout {member}", ephemeral=True)

    embed = discord.Embed(title="New timeout", color=discord.Color.yellow())
    embed.add_field(name="Utente", value=member.mention, inline=False)
    embed.add_field(name="Timeoutato da", value=interaction.user.mention, inline=False)
    embed.add_field(name="Durata", value=time, inline=False)
    embed.add_field(name="Motivo", value=reason, inline=False)
    embed.set_footer(icon_url=ICONACROM, text="Powered by Acrom")
    embed.set_thumbnail(url=ICONACROM)
    await interaction.response.send_message(embed=embed)

command = timeout
