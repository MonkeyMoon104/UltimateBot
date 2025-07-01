from utils.library.libs import *
from discord import app_commands

@app_commands.command(name="avatar", description="Show the user's avatar")
@app_commands.describe(member="User whose avatar you want to see")
async def avatar(interaction: discord.Interaction, member: discord.Member = None):
    user = member or interaction.user

    try:
        user = await interaction.client.fetch_user(user.id)

        avatar_url = user.avatar.url

        if avatar_url:
            embed = discord.Embed(
                title=f"Avatar",
                description=f"[Avatar url]({avatar_url})",
                color=discord.Color.blue()
            )
            embed.set_image(url=avatar_url)
            embed.set_author(name=f"{user.name}", icon_url=user.avatar.url)
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            await interaction.response.send_message(f"L'utente {user.name} non ha un banner", ephemeral=True)
    except discord.NotFound:
        await interaction.response.send_message("Utente non trovato", ephemeral=True)

command = avatar