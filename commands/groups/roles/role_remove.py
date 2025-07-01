from utils.library.libs import *
from data.config import ICONACROM
from discord import app_commands

@app_commands.command(name="remove", description="Rimuove il ruolo specificato ad un membro")
@app_commands.describe(member="Membro al quale vuoi rimuovere il ruolo", role="Ruolo da rimuovere")
async def role_remove(interaction: discord.Interaction, member: discord.Member, role: discord.Role):
    if interaction.user.guild_permissions.administrator or interaction.user.guild_permissions.manage_roles or interaction.user.guild_permissions.manage_guild:
        await interaction.response.send_message(f"Inizio rimozione del ruolo {role.mention} da {member.mention}!", ephemeral=True)

        success, errors = 0, 0
        try:
            if role.position < max(r.position for r in member.roles):
                await member.remove_roles(role)
                success += 1
            else:
                errors += 1
        except (discord.Forbidden, discord.HTTPException):
            errors += 1

        embed = discord.Embed(title="Role-remove Completed", color=discord.Color.green())
        embed.add_field(name="User", value=member.mention, inline=False)
        embed.add_field(name="Success", value=success, inline=False)
        embed.add_field(name="Failed", value=errors, inline=False)
        embed.set_footer(icon_url=ICONACROM, text="Powered by Acrom")
        embed.set_thumbnail(url=ICONACROM)
        await interaction.followup.send(embed=embed, ephemeral=True)
    else:
        embed = discord.Embed(title="Role-remove Error", color=discord.Color.red())
        embed.add_field(name="Error", value="Non hai il permesso per eseguire questo comando", inline=False)
        embed.set_footer(icon_url=ICONACROM, text="Powered by Acrom")
        embed.set_thumbnail(url=ICONACROM)
        await interaction.response.send_message(embed=embed, ephemeral=True)
