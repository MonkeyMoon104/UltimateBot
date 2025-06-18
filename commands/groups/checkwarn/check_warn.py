import discord
from discord import app_commands
from utils.db_utils import connect_to_database
from data.config import STAFF_ROLE_ID, ICONACROM

class CheckWarnCommand(app_commands.Command):
    def __init__(self):
        super().__init__(
            name="warn",
            description="Controlla i warn di un membro dello staff",
            callback=self.callback
        )

    @app_commands.describe(staffer="Seleziona il membro dello staff")
    async def callback(self, interaction: discord.Interaction, staffer: discord.Member):
        if STAFF_ROLE_ID not in [role.id for role in interaction.user.roles]:
            await interaction.response.send_message("❌ Non hai i permessi per eseguire questo comando.", ephemeral=True)
            return

        conn = connect_to_database()
        if conn is None:
            await interaction.response.send_message("Errore nel collegamento al database.", ephemeral=True)
            return

        cursor = conn.cursor()

        cursor.execute("SELECT warn, max_warns FROM warn_staff WHERE staffer = %s", (staffer.id,))
        result = cursor.fetchone()

        if result:
            warn, max_warns = result
            embed = discord.Embed(title="📊 Controllo Warn", color=discord.Color.blue())
            embed.add_field(name="Staffer", value=staffer.mention, inline=False)
            embed.add_field(name="Warn Totali", value=f"{warn}/{max_warns}", inline=False)
            embed.set_thumbnail(url=ICONACROM)
            embed.set_footer(text="Powered by Acrom", icon_url=ICONACROM)
        else:
            embed = discord.Embed(title="📊 Controllo Warn", color=discord.Color.blue())
            embed.add_field(name="Staffer", value=staffer.mention, inline=False)
            embed.add_field(name="Warn Totali", value="0/3 (Nessun warn registrato)", inline=False)
            embed.set_thumbnail(url=ICONACROM)
            embed.set_footer(text="Powered by Acrom", icon_url=ICONACROM)

        await interaction.response.send_message(embed=embed)

        cursor.close()
        conn.close()
