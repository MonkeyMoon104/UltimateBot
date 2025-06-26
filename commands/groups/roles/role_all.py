import discord
from discord import app_commands
from utils.func_utils import add_roles_in_batches
from data.config import ICONACROM, HEADSTAFF_ROLE_ID

@app_commands.command(name="all", description="Aggiunge il ruolo specificato a tutti i membri del server")
@app_commands.describe(role="Ruolo che vuoi assegnare a tutti i membri del server")
async def role_all(interaction: discord.Interaction, role: discord.Role):
    if HEADSTAFF_ROLE_ID in [r.id for r in interaction.user.roles]:
        members = interaction.guild.members
        members_to_assign = [m for m in members if role not in m.roles]
        success, errors = 0, 0

        await interaction.response.send_message(f"Inizio assegnazione a {len(members_to_assign)} membri del server il ruolo: {role.mention}!", ephemeral=True)

        members = [m for m in interaction.guild.members if role not in m.roles]

        success, errors = await add_roles_in_batches(members, role, batch_size=20, delay=5)


        embed = discord.Embed(title="Role-all Completed", color=discord.Color.green())
        embed.add_field(name="User", value=len(members_to_assign), inline=False)
        embed.add_field(name="Success", value=success, inline=False)
        embed.add_field(name="Failed", value=errors, inline=False)
        embed.set_footer(icon_url=ICONACROM, text="Powered by Acrom")
        embed.set_thumbnail(url=ICONACROM)
        await interaction.followup.send(embed=embed, ephemeral=True)
    else:
        embed = discord.Embed(title="Role-all Error", color=discord.Color.red())
        embed.add_field(name="Error", value="Non hai il permesso per eseguire questo comando", inline=False)
        embed.set_footer(icon_url=ICONACROM, text="Powered by Acrom")
        embed.set_thumbnail(url=ICONACROM)
        await interaction.response.send_message(embed=embed, ephemeral=True)
