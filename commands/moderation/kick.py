import discord
from discord import app_commands
from data.config import ICONACROM

@app_commands.command(name="kick", description="Espelli un utente")
@app_commands.describe(member="Utente che vuoi kickare", reason="Motivo del kick")
async def kick(interaction: discord.Interaction, member: discord.Member, *, reason: str):
    await interaction.response.defer(ephemeral=True)  # Deferisce la risposta

    if interaction.user.guild_permissions.kick_members or \
       interaction.user.guild_permissions.ban_members or \
       interaction.user.guild_permissions.administrator:

        try:
            await member.kick(reason=reason)
            embed = discord.Embed(title="New Kick", color=discord.Color.yellow())
            embed.add_field(name="Utente Kickato", value=member.mention, inline=False)
            embed.add_field(name="Kickato da", value=interaction.user.mention, inline=False)
            embed.add_field(name="Motivo", value=reason, inline=False)
        except discord.Forbidden:
            embed = discord.Embed(
                title="Errore",
                description="Non ho il permesso per kickare questo utente.",
                color=discord.Color.red()
            )
    else:
        embed = discord.Embed(
            title="Permessi Mancanti",
            description="Non hai il permesso per usare questo comando.",
            color=discord.Color.red()
        )

    embed.set_footer(icon_url=ICONACROM, text="Powered by Acrom")
    embed.set_thumbnail(url=ICONACROM)
    await interaction.followup.send(embed=embed, ephemeral=True)

command = kick
