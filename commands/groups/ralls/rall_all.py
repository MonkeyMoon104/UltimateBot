import discord
from discord import app_commands
from utils.func_utils import remove_roles_in_batches
from data.config import ICONACROM, HEADSTAFF_ROLE_ID

@app_commands.command(name="all", description="Rimuove il ruolo specificato da tutti i membri del server")
@app_commands.describe(role="Ruolo da rimuovere a tutti gli utenti")
async def rall_all(interaction: discord.Interaction, role: discord.Role):
    if HEADSTAFF_ROLE_ID in [r.id for r in interaction.user.roles]:
        members = [m for m in interaction.guild.members if role in m.roles]

        await interaction.response.send_message(
            f"Inizio rimozione ruolo da {len(members)} membri, batch da 20...", ephemeral=True
        )

        success, errors = await remove_roles_in_batches(members, role, batch_size=20, delay=2)

        embed = discord.Embed(title="Rimozione completata", color=discord.Color.green())
        embed.add_field(name="Totale membri con ruolo", value=len(members), inline=False)
        embed.add_field(name="Successi", value=success, inline=True)
        embed.add_field(name="Fallimenti", value=errors, inline=True)
        embed.set_footer(icon_url=ICONACROM, text="Powered by Acrom")
        embed.set_thumbnail(url=ICONACROM)
        await interaction.followup.send(embed=embed, ephemeral=True)
    else:
        embed = discord.Embed(title="Errore permessi", color=discord.Color.red())
        embed.add_field(name="Errore", value="Non hai il permesso per eseguire questo comando", inline=False)
        embed.set_footer(icon_url=ICONACROM, text="Powered by Acrom")
        embed.set_thumbnail(url=ICONACROM)
        await interaction.response.send_message(embed=embed, ephemeral=True)

