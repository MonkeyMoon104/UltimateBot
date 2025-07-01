from utils.library.libs import *
from discord import app_commands
from data.config import STAFF_ROLE_ID, ICONACROM

class CheckWarningsCommand(app_commands.Command):
    def __init__(self):
        super().__init__(
            name="warnings",
            description="Mostra tutti gli staffer che hanno almeno 1 warn",
            callback=self.callback
        )

    async def callback(self, interaction: discord.Interaction):
        if STAFF_ROLE_ID not in [role.id for role in interaction.user.roles]:
            await interaction.response.send_message("❌ Non hai i permessi per eseguire questo comando.", ephemeral=True)
            return
        
        conn = connect_to_database()
        if conn is None:
            await interaction.response.send_message("Errore nel collegamento al database.", ephemeral=True)
            return

        cursor = conn.cursor()

        try:
            cursor.execute("SELECT staffer, warn, max_warns FROM warn_staff WHERE warn > 0")
            results = cursor.fetchall()

            if results:
                embed = discord.Embed(title="📋 Warn Staff", color=discord.Color.orange())
                embed.set_thumbnail(url=ICONACROM)
                embed.set_footer(text="Powered by Acrom", icon_url=ICONACROM)
                for row in results:
                    staffer_id, warn, max_warns = row
                    staffer = interaction.guild.get_member(int(staffer_id))
                    if staffer:
                        embed.add_field(name=staffer.display_name, value=f"{warn}/{max_warns} warn", inline=False)
                    else:
                        embed.add_field(name=f"ID {staffer_id}", value=f"{warn}/{max_warns} warn - Membro non trovato", inline=False)
            else:
                embed = discord.Embed(title="📋 Warn Staff", color=discord.Color.orange())
                embed.description = "Nessuno staffer ha warn registrati."
                embed.set_thumbnail(url=ICONACROM)
                embed.set_footer(text="Powered by Acrom", icon_url=ICONACROM)

            await interaction.response.send_message(embed=embed)

        except Exception as e:
            await interaction.response.send_message(f"Errore: {e}", ephemeral=True)

        finally:
            cursor.close()
            conn.close()
