from utils.library.libs import *
from data.config import ICONACROM, HEADSTAFF_ROLE_ID
from discord import app_commands

@app_commands.command(name="in", description="Rimuovi un ruolo a tutti i membri con un ruolo base specificato.")
@app_commands.describe(base_role="Ruolo base per selezionare i membri", role_to_remove="Ruolo da rimuovere")
async def rall_in(interaction: discord.Interaction, base_role: discord.Role, role_to_remove: discord.Role):
    if HEADSTAFF_ROLE_ID not in [r.id for r in interaction.user.roles]:
        embed = discord.Embed(title="Rall-in Error", color=discord.Color.red())
        embed.add_field(name="Errore", value="Non hai il permesso per eseguire questo comando.", inline=False)
        embed.set_footer(icon_url=ICONACROM, text="Powered by Acrom")
        embed.set_thumbnail(url=ICONACROM)
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return

    members = [m for m in interaction.guild.members if base_role in m.roles and role_to_remove in m.roles]
    success, errors = 0, 0

    await interaction.response.send_message(
        f"Inizio rimozione del ruolo {role_to_remove.mention} da {len(members)} membri con il ruolo {base_role.mention}!",
        ephemeral=True
    )

    for member in members:
        try:
            await member.remove_roles(role_to_remove)
            success += 1
        except (discord.Forbidden, discord.HTTPException):
            errors += 1

    embed = discord.Embed(title="Rall-in Completed", color=discord.Color.green())
    embed.add_field(name="Totale Membri", value=len(members), inline=False)
    embed.add_field(name="Rimozioni Riuscite", value=success, inline=False)
    embed.add_field(name="Errori", value=errors, inline=False)
    embed.set_footer(icon_url=ICONACROM, text="Powered by Acrom")
    embed.set_thumbnail(url=ICONACROM)
    await interaction.followup.send(embed=embed, ephemeral=True)
