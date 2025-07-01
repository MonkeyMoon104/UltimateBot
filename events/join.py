from utils.library.libs import *
from data.config import WELCOME_CHANNEL_ID, GUILD_ID, WELCOME_RULE_CHANNEL_ID

async def handle_member_join(member: discord.Member, client: discord.Client):
    image_buffer = create_welcome_image(member)

    welcome_channel = client.get_channel(WELCOME_CHANNEL_ID)

    if welcome_channel:
        file = discord.File(fp=image_buffer, filename="welcome.png")
        await welcome_channel.send(
            content=f"### ʙᴇɴᴠᴇɴᴜᴛᴏ/ᴀ {member.mention} ɴᴇʟ ꜱᴇʀᴠᴇʀ, ʀɪᴄᴏʀᴅᴀᴛɪ ᴅɪ ʟᴇɢɢᴇʀᴇ ʟᴇ [ʀᴇɢᴏʟᴇ](https://discord.com/channels/{GUILD_ID}/{WELCOME_RULE_CHANNEL_ID}) ᴇ ᴅɪ ᴅɪᴠᴇʀᴛɪʀᴛɪ!",
            file=file
        )
