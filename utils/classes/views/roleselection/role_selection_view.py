import discord

class RoleSelectionView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Ping Suggestion", style=discord.ButtonStyle.blurple, custom_id="changelogs_button", emoji="<:puntodidomanda:1284513647435055135>")
    async def changelogs_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.toggle_role(interaction, "Ping Suggestion")

    @discord.ui.button(label="Ping TexturePack", style=discord.ButtonStyle.blurple, custom_id="hypeparty_button", emoji="📦")
    async def hypeparty_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.toggle_role(interaction, "Ping TexturePack")

    @discord.ui.button(label="Ping Partner", style=discord.ButtonStyle.blurple, custom_id="news_button", emoji="<:partner:1300598809218519214>")
    async def news_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.toggle_role(interaction, "Ping Partner")

    @discord.ui.button(label="Ping Giveaway", style=discord.ButtonStyle.blurple, custom_id="giveaway_button", emoji="<a:Giveaways:1300595673401659432>")
    async def giveaway_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.toggle_role(interaction, "Ping Giveaway")

    async def toggle_role(self, interaction: discord.Interaction, role_name: str):
        guild = interaction.guild
        role = discord.utils.get(guild.roles, name=role_name)

        if role:
            if role in interaction.user.roles:
                try:
                    await interaction.user.remove_roles(role)
                    await interaction.response.send_message(f"Ti ho rimosso il ruolo {role_name}!", ephemeral=True)
                except discord.Forbidden:
                    await interaction.response.send_message("Non ho i permessi per rimuovere il ruolo. Assicurati che il mio ruolo sia sopra quello dei ruoli che stai cercando di rimuovere.", ephemeral=True)
                except discord.HTTPException as e:
                    await interaction.response.send_message(f"Errore durante la rimozione del ruolo: {e}", ephemeral=True)
            else:
                try:
                    await interaction.user.add_roles(role)
                    await interaction.response.send_message(f"Ti ho assegnato il ruolo {role_name}!", ephemeral=True)
                except discord.Forbidden:
                    await interaction.response.send_message("Non ho i permessi per assegnare il ruolo. Assicurati che il mio ruolo sia sopra quello dei ruoli che stai cercando di assegnare.", ephemeral=True)
                except discord.HTTPException as e:
                    await interaction.response.send_message(f"Errore durante l'assegnazione del ruolo: {e}", ephemeral=True)
        else:
            await interaction.response.send_message(f"Il ruolo {role_name} non esiste nel server.", ephemeral=True)
