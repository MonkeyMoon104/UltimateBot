import discord

class VerificationView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.role_id = 1272630530663518359

    @discord.ui.button(label="Verificati", style=discord.ButtonStyle.green, custom_id="verify_button_acrom", emoji="✅")
    async def verify_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        guild = interaction.guild
        role = discord.utils.get(guild.roles, id=self.role_id)
        
        if role:
            if role in interaction.user.roles:
                await interaction.response.send_message("Hai già il ruolo verificato!", ephemeral=True)
            else:
                try:
                    await interaction.user.add_roles(role)
                    await interaction.response.send_message(f"Ti ho assegnato il ruolo {role.name}!", ephemeral=True)
                except discord.Forbidden:
                    await interaction.response.send_message("Non ho i permessi per assegnare il ruolo. Assicurati che il mio ruolo sia sopra quello dei ruoli che stai cercando di assegnare.", ephemeral=True)
                except discord.HTTPException as e:
                    await interaction.response.send_message(f"Errore durante l'assegnazione del ruolo: {e}", ephemeral=True)
        else:
            await interaction.response.send_message(f"Il ruolo con ID {self.role_id} non esiste nel server.", ephemeral=True)
