from utils.library.libs import *
from data.config import ICONACROM
from discord import app_commands

@app_commands.command(name="verification", description="Invia il messaggio di verifica con bottone")
async def verification(interaction: discord.Interaction, channel: discord.TextChannel = None):
    
    if channel is None:
        channel = interaction.channel

    embed = discord.Embed(
        title="🎉 Benvenuto/a nel server! 🎉",
        description=(
            "Per accedere a tutte le stanze, è necessario completare la verifica.\n\n"
            "✅ **Clicca sul pulsante per confermare la tua presenza.**\n\n"
            "💬 Una volta verificato/a, potrai chattare, esplorare e unirti alla community!\n\n"
            "Grazie per essere qui, non vediamo l'ora di conoscerti!"
        ),
        color=discord.Color.green()
    )
    embed.set_thumbnail(url=ICONACROM)
    embed.set_footer(text="Powered by Acrom", icon_url=ICONACROM)

    await interaction.response.send_message(f"✅ Messaggio di verifica inviato in {channel.mention}!", ephemeral=True)
    await channel.send(embed=embed, view=VerificationView())

command = verification
