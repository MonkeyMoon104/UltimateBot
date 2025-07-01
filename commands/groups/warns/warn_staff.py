from utils.library.libs import *
from discord import app_commands
from data.config import MANAGE_WARN_ROLE_ID, STAFF_ROLE_ID, ICONACROM
from utils.func_utils import depex_staff

class WarnStaffCommand(app_commands.Command):
    def __init__(self):
        super().__init__(
            name="staff",
            description="Avvisa un membro dello staff",
            callback=self.callback
        )

    @app_commands.describe(staffer="Seleziona il membro dello staff da avvisare", motivo="Motivo del warn")
    async def callback(self, interaction: discord.Interaction, staffer: discord.Member, motivo: str):

        if not (MANAGE_WARN_ROLE_ID in [role.id for role in interaction.user.roles]):
            await interaction.response.send_message("❌ Non hai i permessi per eseguire questo comando.", ephemeral=True)
            return
        
        if STAFF_ROLE_ID not in [role.id for role in staffer.roles]:
            await interaction.response.send_message(f"❌ Puoi warnare solo gli staffer! {staffer.mention} non presenta il ruolo @staff.", ephemeral=True)
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
            warn += 1

            if warn >= max_warns:
                cursor.execute("UPDATE warn_staff SET warn = %s WHERE staffer = %s", (warn, staffer.id))
                conn.commit()

                embed = discord.Embed(title="🚨 Staff Warnato", color=discord.Color.red())
                embed.add_field(name="Staffer", value=staffer.mention, inline=False)
                embed.add_field(name="Warnato da", value=interaction.user.mention, inline=False)
                embed.add_field(name="Motivo", value=motivo, inline=False)
                embed.add_field(name="Warn Totali", value=f"{warn}/{max_warns}", inline=False)
                embed.set_thumbnail(url=ICONACROM)
                embed.set_footer(text="Powered by Acrom", icon_url=ICONACROM)

                await interaction.response.send_message(embed=embed)
                await depex_staff(interaction, staffer)

                cursor.execute("DELETE FROM warn_staff WHERE staffer = %s", (staffer.id,))
                conn.commit()

                cursor.close()
                conn.close()
                return
            else:
                cursor.execute("UPDATE warn_staff SET warn = %s WHERE staffer = %s", (warn, staffer.id))
                conn.commit()
        else:
            cursor.execute("INSERT INTO warn_staff (staffer, warn, max_warns) VALUES (%s, %s, %s)", (staffer.id, 1, 3))
            conn.commit()
            warn = 1
            max_warns = 3

        embed = discord.Embed(title="🚨 Staff Warnato", color=discord.Color.red())
        embed.add_field(name="Staffer", value=staffer.mention, inline=False)
        embed.add_field(name="Warnato da", value=interaction.user.mention, inline=False)
        embed.add_field(name="Motivo", value=motivo, inline=False)
        embed.add_field(name="Warn Totali", value=f"{warn}/{max_warns}", inline=False)
        embed.set_thumbnail(url=ICONACROM)
        embed.set_footer(text="Powered by Acrom", icon_url=ICONACROM)

        await interaction.response.send_message(embed=embed)

        cursor.close()
        conn.close()