import discord
from data.config import *

class VerificationView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Verificati", style=discord.ButtonStyle.green, custom_id="verify_button_acrom", emoji="✅")
    async def verify_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        guild = interaction.guild
        verified_role = guild.get_role(VERIFICATION_ROLE_ID)
        not_verified_role = guild.get_role(NOT_VERIFIED_ROLE_ID)

        if verified_role is None:
            await interaction.response.send_message("⚠️ Il ruolo verificato non esiste nel server.", ephemeral=True)
            return

        if verified_role in interaction.user.roles:
            await interaction.response.send_message(f"Hai già il ruolo {verified_role.mention}!", ephemeral=True)
            return

        try:
            if not_verified_role and not_verified_role in interaction.user.roles:
                await interaction.user.remove_roles(not_verified_role)

            await interaction.user.add_roles(verified_role)
            await interaction.response.send_message(f"✅ Ti ho assegnato il ruolo {verified_role.mention}!", ephemeral=True)

        except discord.Forbidden:
            await interaction.response.send_message(
                "🚫 Non ho i permessi per modificare i ruoli. Assicurati che il mio ruolo sia sopra quelli che voglio gestire. Contatta un Admin.",
                ephemeral=True
            )
        except discord.HTTPException as e:
            await interaction.response.send_message(f"❌ Errore durante l'assegnazione del ruolo: {e}", ephemeral=True)
