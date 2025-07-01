from utils.library.libs import *
from utils.func_utils import *

class SuggestionButtons(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(style=discord.ButtonStyle.gray, label="⬆️ Concordo", custom_id="concordo")
    async def concordo_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.handle_vote(interaction, "concordo")

    @discord.ui.button(style=discord.ButtonStyle.gray, label="⬇️ Contrario", custom_id="contrario")
    async def contrario_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.handle_vote(interaction, "contrario")

    async def handle_vote(self, interaction: discord.Interaction, action: str):
        voti_suggerimenti = carica_dati_voti()
        message_id = str(interaction.message.id) 
        user_id = str(interaction.user.id) 

        if message_id not in voti_suggerimenti:
            await interaction.response.send_message("Questo suggerimento non è valido o è stato rimosso.", ephemeral=True)
            return

        voti = voti_suggerimenti[message_id]

        if user_id in voti['voters']:
            previous_vote = voti['voters'][user_id]
            if previous_vote == action:
                await interaction.response.send_message(f"Hai già votato {action}.", ephemeral=True)
                return
            else:
                
                if previous_vote == 'concordo':
                    voti['upvotes'] = max(0, voti['upvotes'] - 1)
                elif previous_vote == 'contrario':
                    voti['downvotes'] = max(0, voti['downvotes'] - 1)

        
        voti['voters'][user_id] = action
        if action == 'concordo':
            voti['upvotes'] += 1
        elif action == 'contrario':
            voti['downvotes'] += 1

        voti_suggerimenti[message_id] = voti
        salva_dati_voti(voti_suggerimenti)

        embed = interaction.message.embeds[0]
        embed.set_field_at(index=0, name="Upvotes", value=str(voti['upvotes']), inline=True)
        embed.set_field_at(index=1, name="Downvotes", value=str(voti['downvotes']), inline=True)

        await interaction.response.edit_message(embed=embed)
        await interaction.followup.send(f"Hai correttamente votato {action}.", ephemeral=True)


    @discord.ui.button(style=discord.ButtonStyle.blurple, label="🟢 Accetta", custom_id="accetta_suggerimento")
    async def accetta_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.handle_accept(interaction, "Accettata", discord.Color.green(), "🟢 Accettata")

    @discord.ui.button(style=discord.ButtonStyle.blurple, label="🔴 Rifiuta", custom_id="rifiuta_suggerimento")
    async def rifiuta_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.handle_accept(interaction, "Rifiutata", discord.Color.red(), "🔴 Rifiutata")

    async def handle_accept(self, interaction: discord.Interaction, status: str, color: discord.Color, status_label: str):
        voti_suggerimenti = carica_dati_voti()
        if not (HEADSTAFF_ROLE_ID in [role.id for role in interaction.user.roles]):
            await interaction.response.send_message("Solo gli amministratori possono gestire questo suggerimento.", ephemeral=True)
            return

        message_id = interaction.message.id
        if str(message_id) not in voti_suggerimenti:
            await interaction.response.send_message("Questo suggerimento non è valido o è stato rimosso.", ephemeral=True)
            return

        suggerimento = voti_suggerimenti[str(message_id)]
        autore_id = suggerimento['author']
        autore = interaction.guild.get_member(autore_id)

        voti_suggerimenti[str(message_id)]['stato'] = status
        embed = interaction.message.embeds[0]
        embed.set_field_at(index=2, name="Stato", value=status_label, inline=False)
        embed.color = color

        self.clear_items()
        await interaction.response.edit_message(embed=embed, view=self)
        salva_dati_voti(voti_suggerimenti)

        if autore:
            try:
                url= interaction.message.jump_url
                notification_embed = discord.Embed(
                    title="La tua suggestion è stata aggiornata",
                    description=f"La tua suggestion: `{suggerimento['description']}` è stata {status.lower()}.",
                    color=color
                )
                notification_embed.add_field(
                    name="Guarda il messaggio originale",
                    value=f"[Clicca qui per vedere il messaggio]({url})"
                )
                notification_embed.set_thumbnail(url=ICONACROM)
                notification_embed.set_image(url=ICONBANNER)
                notification_embed.set_footer(text="Powered by Acrom", icon_url=ICONACROM)

                await autore.send(embed=notification_embed, view=SuggestionLink(url_link=url))
            except discord.Forbidden:
                print(f"Non posso inviare un DM a {autore.name}.")

        staff_channel = interaction.guild.get_channel(SUGGESTION_STAFF_LOGS_CHANNEL)
        if staff_channel:
            staff_message = f"{interaction.message.jump_url} è stata {status.lower()} da {interaction.user.mention}."
            await staff_channel.send(staff_message)

        thread_id = suggerimento['thread_id']
        if thread_id:
            thread = interaction.guild.get_thread(thread_id)
            if thread:
                await thread.delete(reason="Suggestion chiusa!")