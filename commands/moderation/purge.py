from utils.library.libs import *
from data.config import ICONACROM
from discord import app_commands

@app_commands.command(name="purge", description="Cancella un numero specifico di messaggi nel canale")
@app_commands.describe(amount="Numero di messaggi da cancellare")
async def purge(interaction: discord.Interaction, amount: int):
    if not (interaction.user.guild_permissions.manage_messages or interaction.user.guild_permissions.administrator or interaction.user.guild_permissions.manage_guild):
        embed = discord.Embed(title="Purge Error", color=discord.Color.red())
        embed.add_field(name="Error", value="Non hai il permesso (administrator, manage_messages, manage_guild)", inline=False)
        embed.set_footer(icon_url=ICONACROM, text="Powered by Acrom")
        embed.set_thumbnail(url=ICONACROM)
        return await interaction.response.send_message(embed=embed, ephemeral=True)

    try:
        await interaction.channel.purge(limit=amount)
        await interaction.response.send_message(f"{amount} messaggi eliminati!", ephemeral=True)
    except Exception as e:
        await interaction.response.send_message(f"Errore durante l'eliminazione: {e}", ephemeral=True)

command = purge