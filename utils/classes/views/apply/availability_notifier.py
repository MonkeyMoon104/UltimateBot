from utils.library.libs import *
from utils.func_utils import *
from discord.ext import tasks

class AvailabilityNotifier:
    def __init__(self, bot):
        self.bot = bot
        self.check_availability.start()

    @tasks.loop(seconds=10)
    async def check_availability(self):
        tz = pytz.timezone("Europe/Rome")
        now = datetime.datetime.now(tz)
        giorno_en = now.strftime("%A")
        giorno = traduci_giorno(giorno_en)
        ora = f"{now.hour}.{now.minute:02d}"

        matches = apply_get_matches(giorno, ora)

        for provino_id, user_id, author_id, channel_id in matches:
            channel = self.bot.get_channel(channel_id)
            user = self.bot.get_user(user_id)
            author = self.bot.get_user(author_id)

            if channel and user and author:
                await channel.send(
                    f"🔔 **È il momento del provino!**\n"
                    f"- {user.mention}\n"
                    f"- {author.mention}"
                )

                try:
                    await user.send(
                        f"🔔 **È il momento del provino con {author.mention}**\n"
                        f"Presentati nel canale: {channel.mention}"
                    )
                except discord.Forbidden:
                    print(f"❌ Impossibile inviare DM a {user} (ID: {user_id})")

                try:
                    await author.send(
                        f"📢 **È il momento del provino con {user.mention}**\n"
                        f"Vai nel canale: {channel.mention}"
                    )
                except discord.Forbidden:
                    print(f"❌ Impossibile inviare DM a {author} (ID: {author_id})")

                apply_delete_availability(provino_id)

    @check_availability.before_loop
    async def before_check(self):
        await self.bot.wait_until_ready()
