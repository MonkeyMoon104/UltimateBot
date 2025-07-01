from utils.library.libs import *

class DeleteButtonView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Delete", style=discord.ButtonStyle.danger, custom_id="delete_thread_button", emoji="❌")
    async def delete_thread(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.guild_permissions.manage_threads:
            self.clear_items()
            await interaction.response.edit_message(view=self)
            await interaction.channel.edit(locked=True)
            await interaction.followup.send(f"Il thread verrà chiuso tra 5 secondi!")
            await asyncio.sleep(5)
            await interaction.channel.delete()
        else:
            await interaction.response.send_message("Non hai i permessi per chiudere questo thread.", ephemeral=True)

    @discord.ui.button(label="Cancel", style=discord.ButtonStyle.green, custom_id="cancel_thread_button", emoji="🙅‍♂️")
    async def cancel_thread(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.guild_permissions.manage_threads:
            self.clear_items()
            await interaction.response.edit_message(view=self)
            await interaction.channel.edit(locked=False)
            await interaction.followup.send("Il thread è stato sbloccato con successo.", ephemeral=True)
        else:
            await interaction.response.send_message("Non hai i permessi per chiudere questo thread.", ephemeral=True)
