import discord
from discord import app_commands
from data.config import ICONACROM
from utils.classes.views.apply.availability_buttons import AvailabilityButtons

@app_commands.command(name="apply_availability", description="Invia un template con le disponibilità per un provino")
@app_commands.describe(
    lunedi="Disponibilità del lunedì",
    martedi="Disponibilità del martedì",
    mercoledi="Disponibilità del mercoledì",
    giovedi="Disponibilità del giovedì",
    venerdi="Disponibilità del venerdì",
    sabato="Disponibilità del sabato",
    domenica="Disponibilità della domenica"
)
async def apply_template(
    interaction: discord.Interaction,
    lunedi: str,
    martedi: str,
    mercoledi: str,
    giovedi: str,
    venerdi: str,
    sabato: str,
    domenica: str
):
    embed = discord.Embed(
        title="📅 Disponibilità Provino",
        description=(
            f"📤 **Richiesta da:** {interaction.user.mention}\n"
            f"🕓 **Fuso orario:** `Europe/Rome`\n\n"
            "**Orari disponibili:**"
        ),
        color=discord.Color.blue()
    )

    embed.add_field(name="Lunedì", value=f"`{lunedi}`", inline=True)
    embed.add_field(name="Martedì", value=f"`{martedi}`", inline=True)
    embed.add_field(name="Mercoledì", value=f"`{mercoledi}`", inline=True)
    embed.add_field(name="Giovedì", value=f"`{giovedi}`", inline=True)
    embed.add_field(name="Venerdì", value=f"`{venerdi}`", inline=True)
    embed.add_field(name="Sabato", value=f"`{sabato}`", inline=True)
    embed.add_field(name="Domenica", value=f"`{domenica}`", inline=True)

    embed.set_footer(text=f"UserID:{interaction.user.id}")
    embed.set_thumbnail(url=ICONACROM)

    await interaction.response.send_message(embed=embed, view=AvailabilityButtons())

command = apply_template
