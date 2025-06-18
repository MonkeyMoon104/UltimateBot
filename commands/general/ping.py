import discord
from discord import app_commands

@app_commands.command(name="ping", description="Visualizza il ping del bot")
async def ping(interaction: discord.Interaction):
    latency = round(interaction.client.latency * 1000)
    await interaction.response.send_message(f"Pong!🏓 Latenza: _{latency}_ ms", ephemeral=True)

command = ping