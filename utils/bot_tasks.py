import discord
from discord.ext import tasks
from mcstatus import JavaServer
from data.config import *

client = None

@tasks.loop(seconds=15)
async def update_discord_member_count():
    total_members = sum(len(guild.members) for guild in client.guilds)
    activity = discord.Activity(type=discord.ActivityType.watching, name=f"{total_members} membri totali sul discord")
    await client.change_presence(status=discord.Status.idle, activity=activity)

@tasks.loop(seconds=15)
async def update_minecraft_player_count():
    server = JavaServer.lookup(MINECRAFT_SERVER)
    try:
        status = server.status()
        player_count = status.players.online
        max_players = status.players.max
        activity = discord.Activity(type=discord.ActivityType.watching, name=f"{player_count} player's online on AcromMC")
        await client.change_presence(status=discord.Status.do_not_disturb, activity=activity)
    except Exception as e:
        print(f"Errore durante il recupero delle informazioni dal server Minecraft: {e}")
        activity = discord.Activity(type=discord.ActivityType.playing, name=f"Acrom")
        await client.change_presence(status=discord.Status.do_not_disturb, activity=activity)

@tasks.loop(seconds=10)
async def update_bot_presence():
    await update_discord_member_count()
    await update_minecraft_player_count()

def setup(client_ref):
    global client
    client = client_ref
    update_discord_member_count.start()
    update_minecraft_player_count.start()
    update_bot_presence.start()
