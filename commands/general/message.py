import discord
from discord import app_commands
from data.config import *

@app_commands.command(name="message", description="Invia un messaggio privato a un utente")
@app_commands.describe(utente="L'utente a cui inviare il messaggio", messaggio="Il messaggio da inviare")
async def message(interaction: discord.Interaction, utente: discord.Member, messaggio: str):

    if not (interaction.user.guild_permissions.administrator or STAFF_ROLE_ID in [role.id for role in interaction.user.roles]):
        await interaction.response.send_message("❌ Non hai i permessi per eseguire questo comando.", ephemeral=True)
        return

    try:
        await utente.send(messaggio)
        await interaction.response.send_message(f"✅ Messaggio inviato con successo a {utente.mention}.", ephemeral=True)
    except discord.Forbidden:
        await interaction.response.send_message(f"❌ Non posso inviare un messaggio a {utente.mention}. Potrebbe aver bloccato i DM.", ephemeral=True)
    except Exception as e:
        await interaction.response.send_message(f"❌ Si è verificato un errore durante l'invio del messaggio: {str(e)}", ephemeral=True)

command = message