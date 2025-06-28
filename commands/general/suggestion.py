import discord
from discord import app_commands
from data.config import *
import pytz
import datetime
from utils.classes.views.suggestion.suggestion_view import SuggestionButtons
from utils.func_utils import carica_dati_voti, salva_dati_voti

voti_suggerimenti = carica_dati_voti()

@app_commands.command(name="suggerimento", description="Crea un suggerimento")
@app_commands.describe(suggest="Crea una suggerimento!")
async def suggest(interaction: discord.Interaction, suggest: str):

    italy_timezone = pytz.timezone('Europe/Rome')
    current_time_italy = datetime.datetime.now(italy_timezone)
    formatted_time = current_time_italy.strftime('%Y-%m-%d %H:%M:%S')

    embed_suggestion = discord.Embed(
        title="Nuovo Suggerimento",
        description=f"`{suggest}`",
        color=discord.Color.blue()
    )
    embed_suggestion.set_footer(text=f"Suggerimento creato da {interaction.user.name}", icon_url=ICONACROM)

    if any(
        v['description'] == suggest and v['author'] == interaction.user.id
        for v in voti_suggerimenti.values()
    ):
        await interaction.response.send_message("Hai già creato un suggerimento con lo stesso contenuto.", ephemeral=True)
        return

    embed_suggestion.add_field(name="Upvotes ⬆️", value="0", inline=True)
    embed_suggestion.add_field(name="Downvotes ⬇️", value="0", inline=True)
    embed_suggestion.add_field(name="Stato 🔰", value="In attesa 🟠", inline=False)
    embed_suggestion.add_field(name="Data 🗓️", value=formatted_time, inline=False)
    embed_suggestion.set_thumbnail(url=ICONACROM)
    embed_suggestion.set_image(url=ICONBANNER)

    view = SuggestionButtons()
    await interaction.response.send_message(content="<@&1300593039374290984>", embed=embed_suggestion, view=view)

    thread = await interaction.channel.create_thread(
        name=f"Discussione suggestion di {interaction.user.name}",
        type=discord.ChannelType.public_thread,
        slowmode_delay=2
    )

    message = await interaction.original_response()

    voti_suggerimenti[str(message.id)] = {
        'description': suggest,
        'author': interaction.user.id,
        'upvotes': 0,
        'downvotes': 0,
        'voters': {},
        'stato': 'In attesa',
        'thread_id': thread.id
    }

    salva_dati_voti(voti_suggerimenti)

    staff_channel = interaction.guild.get_channel(SUGGESTION_STAFF_LOGS_CHANNEL)
    if staff_channel:
        staff_message = f"Nuovo suggerimento creato: {message.jump_url}; autore: {interaction.user.mention}."
        await staff_channel.send(staff_message)

command = suggest