from utils.library.libs import *
from data.config import HEADSTAFF_ROLE_ID, ICONACROM
from discord import app_commands
from utils.func_utils import lista_tutti_i_provini


@app_commands.command(name="apply-list", description="🔍 Mostra tutti i provini salvati (solo admin)")
async def provini_debug(interaction: discord.Interaction):
    if (interaction.user.guild_permissions.administrator or HEADSTAFF_ROLE_ID in [role.id for role in interaction.user.roles]):
        provini = lista_tutti_i_provini()

        if not provini:
            await interaction.response.send_message("📭 Nessun provino salvato nel database.", ephemeral=True)
            return

        descrizioni = []
        for p in provini:
            provino_id, user_id, author_id, channel_id, giorno, ora = p
            descrizioni.append(
                f"🆔 `{provino_id}` | 👤 User: <@{user_id}> | 👨‍💼 Autore: <@{author_id}>\n"
                f"📅 {giorno} 🕐 {ora} | 📢 Canale: <#{channel_id}>"
            )

        chunks = [descrizioni[i:i+10] for i in range(0, len(descrizioni), 10)]
        for idx, chunk in enumerate(chunks):
            embed = discord.Embed(
                title=f"📋 Provini nel database (pagina {idx+1})",
                description="\n\n".join(chunk),
                color=discord.Color.teal()
            )
            await interaction.followup.send(embed=embed, ephemeral=True) if idx > 0 else await interaction.response.send_message(embed=embed, ephemeral=True)

    else:
        embedapplyerror = discord.Embed(title="apply-list Error", color=discord.Color.red())
        embedapplyerror.add_field(name="Error", value="Non hai il permesso (administrator) per eseguire questo comando", inline=False)
        embedapplyerror.set_footer(icon_url=ICONACROM, text="Powered by Acrom")
        embedapplyerror.set_thumbnail(url=ICONACROM)
        await interaction.response.send_message(embed=embedapplyerror, ephemeral=True)

command = provini_debug