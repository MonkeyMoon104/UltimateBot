import discord

from utils.classes.views.ticket.modal.ticket_info_modal import TicketInfoModal
from data.config import *

class TicketSelect(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="Supporto Generale", description="Richiedi supporto generale", emoji="<a:thinking:1303403456098209875>"),
            discord.SelectOption(label="Store", description="Problema con pagamenti o store", emoji="<a:shopping:1303399120081522771>"),
            discord.SelectOption(label="Report", description="Crea un report verso qualcuno", emoji="<a:warning1:1303402747311161454>"),
            discord.SelectOption(label="Rollback", description="Hai bisogno di un rollback", emoji="<a:Chest:1303404173793951845>"),
            discord.SelectOption(label="Contestazione Ban/Mute", description="Contesta una sanzione", emoji="<a:warning:1303400212588662866>"),
            #discord.SelectOption(label="Discord Account", description="Collega il tuo account discord con minecraft", emoji="<a:Discord_:1303122724742365234>"),
            discord.SelectOption(label="Altro", description="Qualsiasi altra richiesta", emoji="<a:hyper_question_mark:1303402770883154001>")
        ]

        super().__init__(placeholder="Seleziona il tipo di ticket...", min_values=1, max_values=1, options=options, custom_id="persistent_ticket_select")

    async def callback(self, interaction: discord.Interaction):
        selected_option = self.values[0]
        category_name = CATEGORY_DICT.get(selected_option, "Tickets Altro")

        category = discord.utils.get(interaction.guild.categories, name=category_name)

        if category is None:
            category = await interaction.guild.create_category(category_name)

        existing_ticket = discord.utils.get(interaction.guild.text_channels, topic=f"Ticket open by {interaction.user.id}")
        if existing_ticket:
            embedticketexisting = discord.Embed(
                title="Ticket Già Aperto",
                description=f"Puoi trovarlo in {existing_ticket.mention} ✅",
                color=discord.Color.yellow()
            )
            embedticketexisting.set_author(name=f"{interaction.user.name}", icon_url=interaction.user.avatar.url if interaction.user.avatar else ICONACROM)
            embedticketexisting.set_footer(icon_url=ICONACROM, text="Powered by Acrom")

            await interaction.response.send_message(embed=embedticketexisting, ephemeral=True)
            return

        #minecraft_connected, minecraft_name = await check_minecraft_connection(interaction.user)
        modal = TicketInfoModal(selected_option, interaction.user, minecraft_name_value=None)#minecraft_name if minecraft_connected else None)
        await interaction.response.send_modal(modal)

class TicketSelectView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(TicketSelect())