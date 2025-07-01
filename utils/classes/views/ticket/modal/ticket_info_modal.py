from data.config import *
from utils.library.libs import *

italy_timezone = pytz.timezone('Europe/Rome')

class TicketInfoModal(discord.ui.Modal, title="Dettagli Ticket"):
    def __init__(self, ticket_type, user, minecraft_name_value=None):
        super().__init__()
        self.ticket_type = ticket_type
        self.user = user
        self.minecraft_name_value = minecraft_name_value
        self.minecraft_name = discord.ui.TextInput(
            style=discord.TextStyle.short,
            label="Nome Minecraft",
            required=True,
            max_length=100,
            placeholder="Inserisci il tuo nome Minecraft"
        )
        
        self.problem_description = discord.ui.TextInput(
            style=discord.TextStyle.long,
            label="Descrivi il tuo problema",
            required=True,
            max_length=500,
            min_length=5,
            placeholder="Inserisci qui una descrizione dettagliata del tuo problema"
        )

        if self.minecraft_name_value is None:
            self.add_item(self.minecraft_name)

        if self.ticket_type != "Discord Account":
            self.problem_modality = discord.ui.TextInput(
                style=discord.TextStyle.short,
                label="Modalità",
                required=True,
                max_length=100,
                min_length=4,
                placeholder="Scrivi in quale modalità es. (Fazioni)"
            )
            self.add_item(self.problem_modality)
        
        self.add_item(self.problem_description)

    async def on_submit(self, interaction: discord.Interaction):
        category_name = CATEGORY_DICT.get(self.ticket_type, "Tickets Altro")

        category = discord.utils.get(interaction.guild.categories, name=category_name)

        user_name = interaction.user.name
        ticket_channel = await category.create_text_channel(
            name=f"ticket-{user_name}-{self.ticket_type.lower().replace(' ', '-')}",
            topic=f"Ticket open by {interaction.user.id}"
        )

        ticket_support_role = interaction.guild.get_role(TICKET_ROLE_ID)

        await ticket_channel.set_permissions(interaction.guild.default_role, view_channel=False)
        await ticket_channel.set_permissions(interaction.user, send_messages=True, read_message_history=True, view_channel=True)

        embedticketwelcome = discord.Embed(color=discord.Color.green())

        if self.ticket_type == "Store":
            head_staff_role = interaction.guild.get_role(HEADSTAFF_ROLE_ID) 
            if head_staff_role:
                if ticket_support_role:
                    await ticket_channel.set_permissions(head_staff_role, send_messages=True, read_message_history=True, view_channel=True)
                    await ticket_channel.set_permissions(ticket_support_role, view_channel=False)
                    embedticketwelcome.set_footer(icon_url=ICONACROM, text="Powered by Acrom (Visibile solo dagli amministratori)")

        elif self.ticket_type == "Discord Account":
            head_staff_role = interaction.guild.get_role(HEADSTAFF_ROLE_ID) 
            ds_gestore_role = interaction.guild.get_role(GESTORE_ACC_DISCORD_ID)
            if head_staff_role:
                if ds_gestore_role:
                    if ticket_support_role:
                        await ticket_channel.set_permissions(head_staff_role, send_messages=True, read_message_history=True, view_channel=True)
                        await ticket_channel.set_permissions(ticket_support_role, view_channel=False)
                        await ticket_channel.set_permissions(ds_gestore_role, send_messages=True, read_message_history=True, view_channel=True)
                        embedticketwelcome.set_footer(icon_url=ICONACROM, text="Powered by Acrom (Visibile solo dagli amministratori e dai Gestori account discord)")

        else:
            if ticket_support_role:
                await ticket_channel.set_permissions(ticket_support_role, send_messages=True, read_message_history=True, view_channel=True)
                embedticketwelcome.set_footer(icon_url=ICONACROM, text="Powered by Acrom")

        if self.minecraft_name_value:
            minecraft_name = f"{self.minecraft_name_value} (Account Collegato)"
        else:
            minecraft_name = f"{self.minecraft_name.value} (Account Non Collegato)"

        if self.ticket_type != "Discord Account":
            embedticketwelcome.add_field(name="", value=f"Il supporto sarà da te al più presto\nPer chiudere il ticket reagisci con l'emoji 🔒\n\n"
                                                        f"**Nome Minecraft**: `{minecraft_name}`\n"
                                                        f"**Categoria**: `{self.ticket_type}`\n"
                                                        f"**Modalità**: `{self.problem_modality.value}`\n"
                                                        f"**Descrizione**: `{self.problem_description.value}`")
        else:
            embedticketwelcome.add_field(name="", value=f"Il supporto sarà da te al più presto\nPer chiudere il ticket reagisci con l'emoji 🔒\n\n"
                                                        f"**Nome Minecraft**: `{minecraft_name}`\n"
                                                        f"**Categoria**: `{self.ticket_type}`\n"
                                                        f"**Descrizione**: `{self.problem_description.value}`")
        embedticketwelcome.set_thumbnail(url=ICONACROM)
        embedticketwelcome.set_author(name=f"{interaction.user.name}", icon_url=interaction.user.avatar.url if interaction.user.avatar else ICONACROM)
        embedticketwelcome.timestamp = datetime.datetime.now(italy_timezone)

        await ticket_channel.send(content=f"Hey {interaction.user.mention} benvenuto! | {ticket_support_role.mention}", embed=embedticketwelcome, view=CloseClaimTicketButton())

        embedticketcreate = discord.Embed(title="Ticket Creato", description=f"Puoi trovarlo in {ticket_channel.mention} ✅", color=discord.Color.yellow())
        embedticketcreate.set_author(name=f"{interaction.user.name}", icon_url=interaction.user.avatar.url if interaction.user.avatar else ICONACROM)
        embedticketcreate.set_footer(icon_url=ICONACROM, text="Powered by Acrom")

        await interaction.response.send_message(embed=embedticketcreate, ephemeral=True, view=ChannelsTicketLink(server_id=interaction.guild.id, channel_id=ticket_channel.id))
