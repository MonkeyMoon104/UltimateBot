import discord
from discord import app_commands
from data.config import ICONACROM, HEADSTAFF_ROLE_ID

@app_commands.command(name="all", description="Rimuove il ruolo specificato da tutti i membri del server")
@app_commands.describe(role="Ruolo che vuoi rimuovere a tutti gli utenti del server")
async def rall_all(interaction: discord.Interaction, role: discord.Role):
    if HEADSTAFF_ROLE_ID in [r.id for r in interaction.user.roles]:
        members = interaction.guild.members
        success, errors = 0, 0

        await interaction.response.send_message(f"Inizio rimozione a {len(members)} membri del server del ruolo: {role.mention}!", ephemeral=True)

        for member in members:
            try:
                await member.remove_roles(role)
                success += 1
            except (discord.Forbidden, discord.HTTPException):
                errors += 1

        embed = discord.Embed(title="Rall Completed", color=discord.Color.green())
        embed.add_field(name="User", value=len(members), inline=False)
        embed.add_field(name="Success", value=success, inline=False)
        embed.add_field(name="Failed", value=errors, inline=False)
        embed.set_footer(icon_url=ICONACROM, text="Powered by Acrom")
        embed.set_thumbnail(url=ICONACROM)
        await interaction.followup.send(embed=embed, ephemeral=True)
    else:
        embed = discord.Embed(title="Rall Error", color=discord.Color.red())
        embed.add_field(name="Error", value="Non hai il permesso per eseguire questo comando", inline=False)
        embed.set_footer(icon_url=ICONACROM, text="Powered by Acrom")
        embed.set_thumbnail(url=ICONACROM)
        await interaction.response.send_message(embed=embed, ephemeral=True)
