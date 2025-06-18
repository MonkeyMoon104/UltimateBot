import discord
import os
import asyncio
import re
from data.config import *

class CloseClaimTicketButton(discord.ui.View):
    def __init__(self) -> None:
        super().__init__(timeout=None)

    @discord.ui.button(label="Close ticket", emoji="🔒", style=discord.ButtonStyle.red, custom_id="delete_ticket")
    async def delete_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        staff_role_name = TICKET_ROLE_ID
        staff_role = interaction.guild.get_role(staff_role_name)

        if staff_role not in interaction.user.roles:
            await interaction.response.send_message("Non hai il permesso di chiudere il ticket", ephemeral=True)
            return

        self.clear_items()
        await interaction.response.edit_message(view=self)


        creator_id = self.extract_user_id_from_topic(interaction.channel.topic)

        transcript_text = await self.generate_transcript(interaction.channel, staff_role_name)

        file_name = f"transcript-{interaction.channel.name}.txt"

        with open(file_name, "w", encoding="utf-8") as f:
            f.write(transcript_text)

        log_channel = discord.utils.get(interaction.guild.text_channels, name=TRANSCRIPT_TICKET_CHANNEL)
        if log_channel:
            embed = discord.Embed(title="Ticket Chiuso", description=f"Ticket chiuso da {interaction.user.mention}", color=discord.Color.red())
            embed.set_thumbnail(url=ICONACROM)
            await log_channel.send(embed=embed, file=discord.File(file_name))

        if creator_id:
            user = interaction.guild.get_member(int(creator_id))
            if user:
                try:
                    await user.send("Il transcript del tuo ticket è pronto:", file=discord.File(file_name))
                except discord.Forbidden:
                    await interaction.followup.send("Non ho il permesso di inviare in dm il transcript")
            else:
                await interaction.followup.send("Impossibile inviare il transcript all'utente, l'utente non è più presente.")
        else:
            await interaction.followup.send("Impossibile determinare l'utente che ha aperto il ticket dal topic del canale.")

        await interaction.followup.send(f"Il ticket verrà chiuso tra 10 secondi. Salvate eventuali informazioni importanti")

        await asyncio.sleep(10)

        os.remove(file_name)

        await interaction.channel.delete()

    def extract_user_id_from_topic(self, topic):
        if topic:
            match = re.search(r"Ticket open by (\d+)", topic)
            if match:
                return int(match.group(1))
        return None

    async def generate_transcript(self, channel, staff_role_name):
        transcript_text = ""

        staff_role = discord.utils.get(channel.guild.roles, name=staff_role_name)

        async for message in channel.history(limit=None, oldest_first=True):
            timestamp = message.created_at.strftime("%H:%M:%S %d %b %y")
            author = f"{message.author}#{message.author.discriminator}"

            if staff_role in message.author.roles:
                author = f"[STAFF] [{author}]"
            else:
                author = f"[{author}]"

            content = message.clean_content

            transcript_text += f"[{timestamp}] {author} :> {content}\n"

            if message.attachments:
                for attachment in message.attachments:
                    transcript_text += f"[{timestamp}] {author} (Attachment): {attachment.url}\n"

        if not transcript_text.strip():
            transcript_text = "Nessun messaggio nel ticket."

        return transcript_text