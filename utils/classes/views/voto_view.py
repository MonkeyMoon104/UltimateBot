import discord
import validators
import qrcode
import io
from data.config import *

class VotoView(discord.ui.View):
    def __init__(self) -> None:
        super().__init__(timeout=None)

        self.add_item(discord.ui.Button(label="Never Vote", url=VOTE_URL, emoji="🗃️"))

    @discord.ui.button(label="QR Code", emoji="🖇️", style=discord.ButtonStyle.blurple, custom_id="vote_create")
    async def vote_link(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            await interaction.response.send_message(f"⌛ Generando il QR code...", ephemeral=True)

            if not validators.url(VOTE_URL):
                raise ValueError("Invalid URL")

            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.ERROR_CORRECT_L,
                box_size=10,
                border=0,
            )

            qr.add_data(VOTE_URL)
            qr.make(fit=True)

            img = qr.make_image(fill_color="black", back_color="white")

            img_buffer = io.BytesIO()
            img.save(img_buffer, format="PNG")
            img_buffer.seek(0)

            embedqrcode = discord.Embed(
                title="QR Code Vote",
                description=f"Ecco a te il QR code del vote ✅",
                color=discord.Color.yellow()
            )
            embedqrcode.set_author(name=f"Acrom", icon_url=ICONACROM)
            embedqrcode.set_thumbnail(url=ICONACROM)
            embedqrcode.set_footer(icon_url=ICONACROM, text="Powered by Acrom")
            embedqrcode.set_image(url=ICONBANNER)

            file = discord.File(img_buffer, filename="qrcode.png")
            embedqrcode.set_image(url="attachment://qrcode.png")

            await interaction.edit_original_response(content="", embed=embedqrcode, attachments=[file])

        except Exception as e:
            await interaction.edit_original_response(content=f"Error generating QR code: {e}", ephemeral=True)