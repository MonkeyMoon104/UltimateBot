import discord
from discord import app_commands
from data.config import *
from utils.classes.views.roleselection.role_selection_view import RoleSelectionView

@app_commands.command(name="ruoli", description="Seleziona i ruoli")
async def ruoli(interaction: discord.Interaction):

    if not (interaction.user.guild_permissions.administrator or HEADSTAFF_ROLE_ID in [role.id for role in interaction.user.roles]):
        await interaction.response.send_message("❌ Non hai i permessi per eseguire questo comando.", ephemeral=True)
        return    

    channel = interaction.channel

    embed_ruoli = discord.Embed(
        title="Scelta Ruoli",
        description="Clicca uno dei bottoni per ottenere il ruolo corrispondente",
        color=discord.Color.dark_embed(),
    )

    embed_ruoli.add_field(name="Ruoli disponibili", value="<:puntodidomanda:1284513647435055135> - Ping Suggestion\n:package: - Ping TexturePack\n<:partner:1300598809218519214> - Ping Partner\n<a:Giveaways:1300595673401659432> - Ping Giveaway", inline=False)
    embed_ruoli.set_thumbnail(url=ICONACROM)
    embed_ruoli.set_footer(text="Powered by Acrom", icon_url=ICONACROM)

    view = RoleSelectionView()
    await channel.send(embed=embed_ruoli, view=view)
    await interaction.response.send_message("Embed role selection inviato!", ephemeral=True)

command = ruoli