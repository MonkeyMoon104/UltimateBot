from utils.library.libs import os, json, discord, typing, importlib, asyncio, sqlite3, yt_dlp
from collections import deque
from discord import app_commands
from data.config import *

SONG_QUEUES = {}

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

async def remove_roles_in_batches(members, role, batch_size=20, delay=5):
    success, errors = 0, 0

    for i in range(0, len(members), batch_size):
        batch = members[i:i+batch_size]
        
        coros = []
        for member in batch:
            if role in member.roles:
                coros.append(member.remove_roles(role))
            else:
                pass
        
        results = await asyncio.gather(*coros, return_exceptions=True)

        for r in results:
            if isinstance(r, Exception):
                errors += 1
            else:
                success += 1

        await asyncio.sleep(delay)

    return success, errors

async def add_roles_in_batches(members, role, batch_size=20, delay=5):
    success, errors = 0, 0

    for i in range(0, len(members), batch_size):
        batch = members[i:i+batch_size]
        
        coros = []
        for member in batch:
            if role not in member.roles:
                coros.append(member.add_roles(role))
            else:
                pass
        
        results = await asyncio.gather(*coros, return_exceptions=True)

        for r in results:
            if isinstance(r, Exception):
                errors += 1
            else:
                success += 1

        await asyncio.sleep(delay)

    return success, errors

def apply_init_db():
    conn = sqlite3.connect(DB_APPLY_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS provini (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            author_id INTEGER NOT NULL,
            channel_id INTEGER NOT NULL,
            giorno TEXT NOT NULL,
            ora TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def apply_save_availability(user_id: int, author_id: int, channel_id: int, giorno: str, ora: str):
    conn = sqlite3.connect(DB_APPLY_PATH)
    c = conn.cursor()
    c.execute(
        "INSERT INTO provini (user_id, author_id, channel_id, giorno, ora) VALUES (?, ?, ?, ?, ?)",
        (user_id, author_id, channel_id, giorno, ora)
    )
    conn.commit()
    conn.close()

def apply_get_matches(giorno: str, ora: str):
    conn = sqlite3.connect(DB_APPLY_PATH)
    c = conn.cursor()
    c.execute("SELECT id, user_id, author_id, channel_id FROM provini WHERE giorno = ? AND ora = ?", (giorno, ora))
    risultati = c.fetchall()
    conn.close()
    return risultati

def apply_delete_availability(provino_id: int):
    conn = sqlite3.connect(DB_APPLY_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM provini WHERE id = ?", (provino_id,))
    conn.commit()
    conn.close()

def lista_tutti_i_provini():
    conn = sqlite3.connect(DB_APPLY_PATH)
    c = conn.cursor()
    c.execute("SELECT id, user_id, author_id, channel_id, giorno, ora FROM provini")
    risultati = c.fetchall()
    conn.close()
    return risultati


def traduci_giorno(english_day: str):
    giorni = {
        "Monday": "Lunedì",
        "Tuesday": "Martedì",
        "Wednesday": "Mercoledì",
        "Thursday": "Giovedì",
        "Friday": "Venerdì",
        "Saturday": "Sabato",
        "Sunday": "Domenica"
    }
    return giorni.get(english_day, english_day)

async def search_ytdlp_async(query, ydl_opts):
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, lambda: _extract(query, ydl_opts))

def _extract(query, ydl_opts):
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        return ydl.extract_info(query, download=False)
    
async def play_next_song(voice_client, guild_id, channel, client):
    if SONG_QUEUES.get(guild_id) and SONG_QUEUES[guild_id]:
        audio_url, title = SONG_QUEUES[guild_id].popleft()

        ffmpeg_options = {
            "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
            "options": "-vn -b:a 96k -bufsize 128k",
        }

        source = discord.FFmpegOpusAudio(audio_url, **ffmpeg_options, executable="bin\\ffmpeg\\ffmpeg.exe")

        def after_play(error):
            if error:
                print(f"Error playing {title}: {error}")
            asyncio.run_coroutine_threadsafe(
                play_next_song(voice_client, guild_id, channel, client), client.loop
            )

        voice_client.play(source, after=after_play)

        await channel.send(f"▶️ Ora in riproduzione: **{title}**")

    else:
        if voice_client.is_connected():
            await voice_client.disconnect()
        SONG_QUEUES[guild_id] = deque()

