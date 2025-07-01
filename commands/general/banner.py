from utils.library.libs import *
from discord import app_commands

@app_commands.command(name="banner", description="Show the user's banner")
@app_commands.describe(member="User whose banner you want to see")
async def banner(interaction: discord.Interaction, member: discord.Member = None):
    user = member or interaction.user

    try:
        user = await interaction.client.fetch_user(user.id)

        banner_url = user.banner.url if user.banner else None

        if banner_url:
            embed = discord.Embed(
                title=f"Banner",
                description=f"[Banner url]({banner_url})",
                color=discord.Color.blue()
            )
            embed.set_image(url=banner_url)
            embed.set_author(name=f"{user.name}", icon_url=user.avatar.url)
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            await interaction.response.send_message(f"L'utente {user.name} non ha un banner", ephemeral=True)
    except discord.NotFound:
        await interaction.response.send_message("Utente non trovato", ephemeral=True)

command = banner