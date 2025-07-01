from utils.library.libs import *

class CloseButtonThread(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Close", style=discord.ButtonStyle.danger, custom_id="close_thread_button", emoji="🔒")
    async def close_thread(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.guild_permissions.manage_threads:
            await interaction.channel.edit(locked=False)
            await interaction.response.send_message("Il thread è stato chiuso con successo", ephemeral=True)
            await interaction.channel.send("Eliminare il thread?", view=DeleteButtonView())
        else:
            await interaction.response.send_message("Non hai i permessi per chiudere questo thread", ephemeral=True)

    @discord.ui.button(label="Lock", style=discord.ButtonStyle.danger, custom_id="lock_thread_button", emoji="🔐")
    async def lock_thread(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.guild_permissions.manage_threads:
            await interaction.channel.edit(locked=True)
            await interaction.response.send_message("Il thread è stato loockato con successo")
        else:
            await interaction.response.send_message("Non hai i permessi per chiudere questo thread.", ephemeral=True)
