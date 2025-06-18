import json
import os
import discord
import typing
import importlib
from discord import app_commands
from data.config import JSON_FILE_PATH, VOTI_FILE, ROLE_DEPX_ID, ICONACROM, CHANNEL_DEPEX_LOGS

def initialize_json_file():
    if not os.path.isfile(JSON_FILE_PATH):
        with open(JSON_FILE_PATH, 'w') as file:
            json.dump([], file, indent=4)

def load_codes_from_json():
    with open(JSON_FILE_PATH, 'r') as file:
        data = json.load(file)
        if not isinstance(data, list):
            data = []
        return data

def save_codes_to_json(data):
    if not isinstance(data, list):
        data = []
    with open(JSON_FILE_PATH, 'w') as file:
        json.dump(data, file, indent=4)

def carica_dati_voti():
    if os.path.exists(VOTI_FILE):
        try:
            with open(VOTI_FILE, "r") as file:
                data = json.load(file)
                if data is None:
                    return {}
                return data
        except json.JSONDecodeError:
            print("File JSON non valido. Creando un nuovo file.")
            return {}
    return {}

def salva_dati_voti(data):
    with open(VOTI_FILE, "w") as file:
        json.dump(data, file, indent=4)

def crea_file_json_vuoto():
    if not os.path.exists(VOTI_FILE):
        with open(VOTI_FILE, "w") as file:
            json.dump({}, file)

def pulisci_dati_voti():
    try:
        print("Inizio pulizia dei dati.")
        dati_voti = carica_dati_voti()
        print("Dati caricati: %s", dati_voti)
        dati_puliti = {k: v for k, v in dati_voti.items() if v['stato'] == 'In attesa'}
        print("Dati puliti: %s", dati_puliti)
        salva_dati_voti(dati_puliti)
        print("Pulizia completata.")
    except Exception as e:
        print("Errore durante la pulizia dei dati: %s", e)

async def channel_autocomplete(
    interaction: discord.Interaction, current: str
) -> typing.List[app_commands.Choice[str]]:
    channels = [
        channel.name
        for channel in interaction.guild.text_channels
        if channel.topic and "Ticket open by" in channel.topic
    ]
    data = [
        app_commands.Choice(name=channel, value=channel)
        for channel in channels
        if current.lower() in channel.lower()
    ]
    return data

async def depex_staff(interaction: discord.Interaction, staffer: discord.Member):
    roles_to_remove = staffer.roles[1:]
    for role in roles_to_remove:
        await staffer.remove_roles(role)

    depex_role = interaction.guild.get_role(ROLE_DEPX_ID)
    if depex_role:
        await staffer.add_roles(depex_role)

    try:
        await staffer.send("⚠️ Sei stato depexato per aver raggiunto il numero massimo di warn. (prova, non preoccuparti, sono MonkeyMoon104 chill)")
        print("messaggio inviato in privato andato in successo!")
    except discord.Forbidden:
        print("messaggio inviato in privato andato in fallimento")
        pass

    embed = discord.Embed(title="⚠️ Staffer Depexato", color=discord.Color.dark_red())
    embed.add_field(name="Staffer", value=staffer.mention, inline=False)
    embed.add_field(name="Motivo", value="Massimo di warn raggiunto", inline=False)
    embed.set_thumbnail(url=ICONACROM)
    embed.set_footer(text="Powered by Acrom", icon_url=ICONACROM)

    try:
        log_channel = interaction.guild.get_channel(CHANNEL_DEPEX_LOGS)
        if log_channel:
            await log_channel.send(embed=embed)
    except discord.HTTPException:
        await interaction.followup.send(embed=embed, ephemeral=True)

async def load_commands(client):
    base_path = "commands"
    categories = ["moderation", "general"]

    for category in categories:
        command_dir = os.path.join(base_path, category)

        for filename in os.listdir(command_dir):
            if filename.endswith(".py") and not filename.startswith("_"):
                module_name = filename[:-3]
                module_path = f"{base_path}.{category}.{module_name}"

                module = importlib.import_module(module_path)

                if hasattr(module, "command"):
                    client.tree.add_command(module.command)

async def load_context_menus(client):
    base_path = "commands"
    categories = ["context"]

    for category in categories:
        command_dir = os.path.join(base_path, category)

        for filename in os.listdir(command_dir):
            if filename.endswith(".py") and not filename.startswith("_"):
                module_name = filename[:-3]
                module_path = f"{base_path}.{category}.{module_name}"

                module = importlib.import_module(module_path)

                if hasattr(module, "context_menu_command"):
                    client.tree.add_command(module.context_menu_command)
