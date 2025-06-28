import discord
import re
from utils.func_utils import apply_save_availability

class AvailabilityModal(discord.ui.Modal, title="Conferma Orario Disponibilità"):
    def __init__(self, original_embed: discord.Embed):
        super().__init__(timeout=None)

        self.original_embed = original_embed

        orari = [f"{field.name}: {field.value.strip('`')}" for field in original_embed.fields]
        orari_str = "\n".join(orari)

        self.orari_input = discord.ui.TextInput(
            label="Orario",
            placeholder="Inserisci un solo giorno e un orario (es: Martedì: 15.30)",
            default=orari_str,
            style=discord.TextStyle.paragraph,
            required=True,
            max_length=1000
        )

        self.add_item(self.orari_input)

    async def on_submit(self, interaction: discord.Interaction):
        value = self.orari_input.value.strip()

        lines = value.splitlines()
        non_empty_lines = [line.strip() for line in lines if line.strip()]

        if len(non_empty_lines) != 1:
            await interaction.response.send_message(
                "❌ Devi lasciare **solo un giorno e un orario**, es: `Martedì: 15.30`", ephemeral=True
            )
            return

        valid_days = ["Lunedì", "Martedì", "Mercoledì", "Giovedì", "Venerdì", "Sabato", "Domenica"]
        pattern = r"^(" + "|".join(valid_days) + r"): ?(\d{1,2}(?:\.\d{1,2})?)$"
        match = re.fullmatch(pattern, non_empty_lines[0], re.IGNORECASE)

        if not match:
            await interaction.response.send_message(
                "❌ Il formato non è valido o il giorno è scritto male. Usa: `Giorno: ora` (es: `Giovedì: 14.30`)", ephemeral=True
            )
            return

        giorno = match.group(1).capitalize()
        ora = match.group(2)

        original_user_id = None
        if self.original_embed.footer and self.original_embed.footer.text.startswith("UserID:"):
            try:
                original_user_id = int(self.original_embed.footer.text.replace("UserID:", "").strip())
            except ValueError:
                pass

        apply_save_availability(
            user_id=interaction.user.id,
            author_id=original_user_id or interaction.user.id,
            channel_id=interaction.channel.id,
            giorno=giorno,
            ora=ora
        )

        new_embed = discord.Embed(
            title="✅ Disponibilità Confermata",
            description=f"**{giorno}: {ora}**",
            color=discord.Color.green()
        )
        if self.original_embed.footer:
            new_embed.set_footer(text=self.original_embed.footer.text)

        await interaction.message.edit(embed=new_embed, view=None)

        await interaction.response.send_message(
            f"✅ Disponibilità confermata:\n```{giorno}: {ora}```", ephemeral=True
        )
