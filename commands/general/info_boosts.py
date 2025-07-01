from utils.library.libs import *
from data.config import *
from discord import app_commands

@app_commands.command(name="info-boosts", description="Visualizza le informazioni sul boost del server")
async def info_boosts(interaction: discord.Interaction):
    server = interaction.guild

    boost_count = server.premium_subscription_count
    boosters = [member for member in server.members if member.premium_since is not None]
    
    embed = discord.Embed(title=f"Potenziamenti del Server ", color=discord.Color.pink())
    embed.add_field(name="Numero di Potenziamenti ", value=f"{boost_count}", inline=False)
    embed.set_footer(icon_url=ICONACROM, text="Powered by Acrom")
    embed.set_thumbnail(url=ICONACROM)
    
    if boosters:
        boosters_info = ""
        for member in boosters:
            boosts = len([boost for boost in server.premium_subscribers if boost.id == member.id])
            boosters_info += f"{member.mention} - {boosts} boost{'s' if boosts != 1 else ''}\n"
        embed.add_field(name="Boosters", value=boosters_info, inline=False)
    else:
        embed.add_field(name="Boosters", value="Nessun booster al momento", inline=False)
    
    await interaction.response.send_message(embed=embed, ephemeral=True)

command = info_boosts