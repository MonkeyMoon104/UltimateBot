import discord
from discord import app_commands
from data.config import ICONACROM

@app_commands.command(name="add", description="Aggiunge il ruolo specificato al membro del server")
@app_commands.describe(member="Membro alla quale vuoi assegnare il ruolo", role="Ruolo che vuoi assegnare")
async def role_add(interaction: discord.Interaction, member: discord.Member, role: discord.Role):
    if interaction.user.guild_permissions.administrator or interaction.user.guild_permissions.manage_roles or interaction.user.guild_permissions.manage_guild:
        await interaction.response.send_message(f"Inizio assegnazione a {member.mention} del ruolo: {role.mention}!", ephemeral=True)

        success, errors = 0, 0
        try:
            if role.position < max(r.position for r in member.roles):
                await member.add_roles(role)
                success += 1
            else:
                errors += 1
        except (discord.Forbidden, discord.HTTPException):
            errors += 1

        embed = discord.Embed(title="Role-add Completed", color=discord.Color.green())
        embed.add_field(name="User", value=member.mention, inline=False)
        embed.add_field(name="Success", value=success, inline=False)
        embed.add_field(name="Failed", value=errors, inline=False)
        embed.set_footer(icon_url=ICONACROM, text="Powered by Acrom")
        embed.set_thumbnail(url=ICONACROM)
        await interaction.followup.send(embed=embed, ephemeral=True)
    else:
        embed = discord.Embed(title="Role-add Error", color=discord.Color.red())
        embed.add_field(name="Error", value="Non hai il permesso per eseguire questo comando", inline=False)
        embed.set_footer(icon_url=ICONACROM, text="Powered by Acrom")
        embed.set_thumbnail(url=ICONACROM)
        await interaction.response.send_message(embed=embed, ephemeral=True)
