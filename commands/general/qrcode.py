import discord
from discord import app_commands
import validators
import qrcode
import io

@app_commands.command(name='qrcode', description='Generate a QR code for the provided link')
@app_commands.describe(url="The URL of the site for which you want to generate a QR code")
async def generate_qrcode(interaction: discord.Interaction, url: str):
    try:
        if not validators.url(url):
            raise ValueError("Invalid URL")
        
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.ERROR_CORRECT_L,
            box_size=10,
            border=0,
        )
        
        qr.add_data(url)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        
        img_buffer = io.BytesIO()
        img.save(img_buffer, format="PNG")
        img_buffer.seek(0)
        
        await interaction.response.send_message(
            file=discord.File(img_buffer, filename="qrcode.png"),
            ephemeral=True
        )
    except Exception as e:
        await interaction.response.send_message(f"Error generating QR code: {e}", ephemeral=True)

command = generate_qrcode