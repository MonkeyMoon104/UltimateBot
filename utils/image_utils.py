from io import BytesIO
from PIL import Image, ImageFont, ImageDraw
import requests
from data.config import BACKGROUND_PATH, FONT_PATH

def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def create_welcome_image(member):
    background = Image.open(BACKGROUND_PATH).convert("RGBA")

    try:
        font = ImageFont.truetype(FONT_PATH, 110)
    except IOError:
        font = ImageFont.load_default()

    draw = ImageDraw.Draw(background)
    username = member.name
    text_color = hex_to_rgb("#FFD700")

    avatar_url = member.display_avatar.replace(static_format="png", size=512).url
    response = requests.get(avatar_url)
    avatar_image = Image.open(BytesIO(response.content)).convert("RGBA")

    avatar_size = (320, 320)
    avatar_image = avatar_image.resize(avatar_size)
    mask = Image.new("L", avatar_size, 0)
    draw_mask = ImageDraw.Draw(mask)
    draw_mask.ellipse((0, 0) + avatar_size, fill=255)
    avatar_image.putalpha(mask)

    bg_w, bg_h = background.size
    avatar_x = (bg_w - avatar_size[0]) // 2
    avatar_y = int(bg_h * 0.2)
    background.paste(avatar_image, (avatar_x, avatar_y), avatar_image)

    bbox = draw.textbbox((0, 0), username, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    text_x = (bg_w - text_width) // 2
    text_y = bg_h - text_height - 80

    draw.text((text_x, text_y), username, font=font, fill=text_color)

    buffer = BytesIO()
    background.save(buffer, format="PNG")
    buffer.seek(0)

    return buffer
