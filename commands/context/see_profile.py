from utils.library.libs import *
from data.config import *
from discord import app_commands

@app_commands.context_menu(name="See Profile")
async def see_profile(interaction: discord.Interaction, member: discord.Member):
    user = await interaction.client.fetch_user(member.id)

    embed = discord.Embed(
        title=f"Profilo di {member.name}",
        color=discord.Color.blue()
    )
    embed.set_thumbnail(url=ICONACROM)
    embed.set_footer(icon_url=ICONACROM, text="Powered by Acrom")

    view = ProfileViewLinks()

    if user.avatar:
        avatar_format = "gif" if user.avatar.is_animated() else "png"
        url_avatar = user.avatar.replace(format=avatar_format, size=4096).url
        embed.add_field(name="🌍 Avatar Globale", value=f"[Clicca qui]({url_avatar})", inline=False)
        view.add_link("🌍 Avatar Globale", url_avatar)
    else:
        embed.add_field(name="🌍 Avatar Globale", value="Nessun avatar", inline=False)

    if member.display_avatar:
        avatar_server_format = "gif" if member.display_avatar.is_animated() else "png"
        url_server_avatar = member.display_avatar.replace(format=avatar_server_format, size=4096).url
        embed.add_field(name="🏷️ Avatar Server", value=f"[Clicca qui]({url_server_avatar})", inline=False)
        view.add_link("🏷️ Avatar Server", url_server_avatar)

    if user.banner:
        banner_format = "gif" if user.banner.is_animated() else "png"
        url_banner = user.banner.replace(format=banner_format, size=4096).url
        embed.add_field(name="🖼️ Banner", value=f"[Clicca qui]({url_banner})", inline=False)
        embed.set_image(url=url_banner)
        view.add_link("🖼️ Banner", url_banner)
    else:
        embed.add_field(name="🖼️ Banner", value="Nessun banner disponibile", inline=False)

    await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

context_menu_command = see_profile
