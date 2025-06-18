import discord
from discord import app_commands
from data.config import ICONACROM, HEADSTAFF_ROLE_ID

@app_commands.command(name="in", description="Aggiungi un ruolo a tutti i membri con un ruolo base specificato.")
@app_commands.describe(base_role="Ruolo base per selezionare i membri", role_to_add="Ruolo da assegnare")
async def role_in(interaction: discord.Interaction, base_role: discord.Role, role_to_add: discord.Role):
    if HEADSTAFF_ROLE_ID not in [r.id for r in interaction.user.roles]:
        embed = discord.Embed(title="Role Error", color=discord.Color.red(), description="Non hai il permesso per eseguire questo comando.")
        embed.set_footer(icon_url=ICONACROM, text="Powered by Acrom")
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return

    members = [m for m in interaction.guild.members if base_role in m.roles and role_to_add not in m.roles]
    success, errors = 0, 0

    await interaction.response.send_message(f"Inizio assegnazione del ruolo {role_to_add.mention} a {len(members)} membri con il ruolo {base_role.mention}!", ephemeral=True)

    for member in members:
        try:
            await member.add_roles(role_to_add)
            success += 1
        except (discord.Forbidden, discord.HTTPException):
            errors += 1

    embed = discord.Embed(title="Role Command Completed", color=discord.Color.green())
    embed.add_field(name="Membri Totali", value=len(members), inline=False)
    embed.add_field(name="Successi", value=success, inline=False)
    embed.add_field(name="Errori", value=errors, inline=False)
    embed.set_footer(icon_url=ICONACROM, text="Powered by Acrom")
    embed.set_thumbnail(url=ICONACROM)
    await interaction.followup.send(embed=embed, ephemeral=True)
