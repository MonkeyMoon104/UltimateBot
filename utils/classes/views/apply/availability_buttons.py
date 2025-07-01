from utils.library.libs import *

class AvailabilityButtons(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Accetta", style=discord.ButtonStyle.green, custom_id="accept_availability", emoji="✅")
    async def accept(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = interaction.message.embeds[0] if interaction.message.embeds else None

        if not embed:
            await interaction.response.send_message("❌ Impossibile trovare l'embed da modificare.", ephemeral=True)
            return
        
        if embed.footer and embed.footer.text.startswith("UserID:"):
            author_id = int(embed.footer.text.replace("UserID:", "").strip())

            if interaction.user.id == author_id:
                await interaction.response.send_message("❌ Non puoi accettare la tua stessa offertà disponibilità!", ephemeral=True)
                return

        await interaction.response.send_modal(AvailabilityModal(embed))

    @discord.ui.button(label="Rifiuta", style=discord.ButtonStyle.red, custom_id="reject_availability", emoji="❌")
    async def reject(self, interaction: discord.Interaction, button: discord.ui.Button):
        message = interaction.message
        embed = message.embeds[0] if message.embeds else None

        if not embed:
            await interaction.response.send_message("❌ Impossibile trovare l'embed da modificare.", ephemeral=True)
            return

        disabled_view = AvailabilityButtons()
        for child in disabled_view.children:
            if child.custom_id != "edit_availability":
                child.disabled = True

        new_embed = embed.copy()
        new_embed.title = "❌ Disponibilità rifiutate"
        new_embed.color = discord.Color.red()

        await interaction.response.edit_message(embed=new_embed, view=disabled_view)
        await interaction.followup.send("Hai rifiutato le disponibilità.", ephemeral=True)

    @discord.ui.button(label="Cambia disponibilità", style=discord.ButtonStyle.blurple, custom_id="edit_availability", emoji="🔁")
    async def edit(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("📝 Funzione per cambiare disponibilità in arrivo!", ephemeral=True)
