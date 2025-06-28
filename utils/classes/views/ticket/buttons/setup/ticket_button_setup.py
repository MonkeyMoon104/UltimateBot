import discord
from data.config import ICONBANNER
from utils.classes.views.ticket.select.ticket_select import TicketSelectView

class TicketButtonSetup(discord.ui.View):
    def __init__(self) -> None:
        super().__init__(timeout=None)
    
    @discord.ui.button(label="Create", style=discord.ButtonStyle.green, custom_id="create_button")
    async def create_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.clear_items()
        await interaction.response.edit_message(view=self)

        embedticket = discord.Embed(
            title="🎫 | ACROM MC",
            description="👋 | Benvenuto!\nPer garantire un supporto efficiente, ti chiediamo gentilmente di selezionare la motivazione per cui vorresti aprire questo ticket utilizzando il pulsante sottostante.",
            color=discord.Color.yellow()
        )
        embedticket.set_footer(icon_url=ICONBANNER, text="⚠️ | Attenzione! Ti preghiamo di utilizzare i ticket in modo responsabile, l'abuso potrebbe comportare sanzioni, incluso il ban temporaneo o permanente.")
        embedticket.set_thumbnail(url=ICONBANNER)

        await interaction.channel.send(embed=embedticket, view=TicketSelectView())

    @discord.ui.button(label="Cancel", style=discord.ButtonStyle.red, custom_id="no_button")
    async def anull_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.clear_items()
        await interaction.response.edit_message(view=self)
        await interaction.followup.send(content="Action annulled", ephemeral=True)
