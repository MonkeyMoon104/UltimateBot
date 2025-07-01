from utils.library.libs import *
from discord import app_commands
from data.config import HEADSTAFF_ROLE_ID, ICONACROM

class RemoveAllWarnCommand(app_commands.Command):
    def __init__(self):
        super().__init__(
            name="remove-all",
            description="Rimuove tutti gli staffer dal database di warn",
            callback=self.callback
        )

    async def callback(self, interaction: discord.Interaction):
        if not (HEADSTAFF_ROLE_ID in [role.id for role in interaction.user.roles]):
            await interaction.response.send_message("❌ Non hai i permessi per eseguire questo comando.", ephemeral=True)
            return

        conn = connect_to_database()
        if conn is None:
            await interaction.response.send_message("Errore nel collegamento al database.", ephemeral=True)
            return

        cursor = conn.cursor()

        try:
            cursor.execute("DELETE FROM warn_staff")
            conn.commit()

            embed = discord.Embed(title="✅ Tutti i warn rimossi", color=discord.Color.green())
            embed.description = "Tutti gli staffer sono stati rimossi dal database di warn."
            embed.set_thumbnail(url=ICONACROM)
            embed.set_footer(text="Powered by Acrom", icon_url=ICONACROM)

            await interaction.response.send_message(embed=embed)
        except Exception as e:
            await interaction.response.send_message(f"Errore: {e}", ephemeral=True)
        finally:
            cursor.close()
            conn.close()
