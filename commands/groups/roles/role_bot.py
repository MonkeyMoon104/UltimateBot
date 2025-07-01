from utils.library.libs import *
from data.config import ICONACROM, HEADSTAFF_ROLE_ID
from discord import app_commands

@app_commands.command(name="bot", description="Aggiunge il ruolo specificato a tutti i bot del server")
@app_commands.describe(role="Ruolo che vuoi assegnare a tutti i bot del server")
async def role_bot(interaction: discord.Interaction, role: discord.Role):
    if HEADSTAFF_ROLE_ID in [r.id for r in interaction.user.roles]:
        bot_members = [m for m in interaction.guild.members if m.bot and role not in m.roles]
        success, errors = 0, 0

        await interaction.response.send_message(f"Inizio assegnazione a {len(bot_members)} bot del server il ruolo: {role.mention}!", ephemeral=True)

        for member in bot_members:
            try:
                await member.add_roles(role)
                success += 1
            except (discord.Forbidden, discord.HTTPException):
                errors += 1

        embed = discord.Embed(title="Role-bot Completed", color=discord.Color.green())
        embed.add_field(name="Bot", value=len(bot_members), inline=False)
        embed.add_field(name="Success", value=success, inline=False)
        embed.add_field(name="Failed", value=errors, inline=False)
        embed.set_footer(icon_url=ICONACROM, text="Powered by Acrom")
        embed.set_thumbnail(url=ICONACROM)
        await interaction.followup.send(embed=embed, ephemeral=True)
    else:
        embed = discord.Embed(title="Role-bot Error", color=discord.Color.red())
        embed.add_field(name="Error", value="Non hai il permesso per eseguire questo comando", inline=False)
        embed.set_footer(icon_url=ICONACROM, text="Powered by Acrom")
        embed.set_thumbnail(url=ICONACROM)
        await interaction.response.send_message(embed=embed, ephemeral=True)
