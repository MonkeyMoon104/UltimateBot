from utils.library.libs import *
from data.config import TMZ
from discord import app_commands
from utils.func_utils import *

class PlayCommand(app_commands.Command):
    def __init__(self):
        super().__init__(
            name="play",
            description="Inizia una musica",
            callback=self.callback
        )

    @app_commands.describe(song_query="Search query")
    async def callback(self, interaction: discord.Interaction, song_query: str):
        await interaction.response.defer(ephemeral=False)

        if interaction.user.voice is None:
            await interaction.followup.send("Devi essere in un canale vocale per usare questo comando.", ephemeral=False)
            return

        voice_channel = interaction.user.voice.channel
        client = interaction.client

        if voice_channel is None:
            await interaction.followup.send("You must be in a voice channel.", ephemeral=False)
            return

        voice_client = interaction.guild.voice_client
        if voice_client is None:
            voice_client = await voice_channel.connect()
        elif voice_channel != voice_client.channel:
            await voice_client.move_to(voice_channel)

        ydl_options = {
            "format": "bestaudio[abr<=96]/bestaudio",
            "noplaylist": True,
            "youtube_include_dash_manifest": False,
            "youtube_include_hls_manifest": False,
        }

        query = "ytsearch1: " + song_query
        results = await search_ytdlp_async(query, ydl_options)
        tracks = results.get("entries", [])

        if not tracks:
            await interaction.followup.send("Nessun risultato trovato.", ephemeral=False)
            return

        first_track = tracks[0]
        audio_url = first_track["url"]
        title = first_track.get("title", "Sconosciuto")
        thumbnail = first_track.get("thumbnail", "")
        webpage_url = first_track.get("webpage_url", "")
        uploader = first_track.get("uploader", "Sconosciuto")
        duration = first_track.get("duration", 0)
        view_count = first_track.get("view_count", 0)
        like_count = first_track.get("like_count", None)
        upload_date = first_track.get("upload_date", None)
        description = first_track.get("description", "")
        requester = interaction.user

        def format_duration(seconds):
            td = datetime.timedelta(seconds=seconds)
            total_seconds = int(td.total_seconds())
            hours, remainder = divmod(total_seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            if hours > 0:
                return f"{hours}:{minutes:02}:{seconds:02}"
            return f"{minutes}:{seconds:02}"

        rome_tz = ZoneInfo(TMZ)
        now_rome = datetime.datetime.now(tz=rome_tz)
        end_time_rome = now_rome + datetime.timedelta(seconds=duration)
        end_timestamp = int(end_time_rome.timestamp())

        formatted_date = ""
        if upload_date:
            try:
                dt_utc = datetime.datetime.strptime(upload_date, "%Y%m%d").replace(tzinfo=datetime.timezone.utc)
                dt_rome = dt_utc.astimezone(rome_tz)
                formatted_date = dt_rome.strftime("%d %B %Y")
            except:
                formatted_date = upload_date

        guild_id = str(interaction.guild_id)
        if SONG_QUEUES.get(guild_id) is None:
            SONG_QUEUES[guild_id] = deque()
        SONG_QUEUES[guild_id].append((audio_url, title))

        embed = discord.Embed(
            title=title,
            description="🎶 **Aggiunto alla coda**" if voice_client.is_playing() or voice_client.is_paused() else "▶️ **Ora in riproduzione!**",
            color=discord.Color.blurple(),
            url=webpage_url
        )

        embed.set_thumbnail(url=thumbnail)
        embed.add_field(name="👤 Uploader", value=uploader, inline=True)
        embed.add_field(
            name="⏱️ Durata",
            value=f"{format_duration(duration)}" if voice_client.is_paused() or voice_client.is_playing() else f"{format_duration(duration)}\nTermina: <t:{end_timestamp}:R>",
            inline=True
        )
        embed.add_field(name="👁️ Visualizzazioni", value=f"{view_count:,}", inline=True)

        if like_count is not None:
            embed.add_field(name="👍 Mi piace", value=f"{like_count:,}", inline=True)

        if formatted_date:
            embed.add_field(name="📅 Pubblicato il", value=formatted_date, inline=True)

        if description:
            short_desc = (description[:200] + "...") if len(description) > 200 else description
            embed.add_field(name="🧾 Descrizione", value=f"```{short_desc}```", inline=False)

        embed.set_footer(text=f"Richiesto da {requester.display_name}", icon_url=requester.display_avatar.url)

        await interaction.followup.send(embed=embed)

        if not (voice_client.is_playing() or voice_client.is_paused()):
            await play_next_song(voice_client, guild_id, interaction.channel, client)
