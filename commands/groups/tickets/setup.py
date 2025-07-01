from utils.library.libs import *
from discord import app_commands
from data.config import ICONACROM, HEADSTAFF_ROLE_ID
from discord import app_commands


class SetupCommand(app_commands.Command):
    def __init__(self):
        super().__init__(name="setup", description="Setup ticket", callback=self.callback)

    async def callback(self, interaction: discord.Interaction):
        if (interaction.user.guild_permissions.administrator or HEADSTAFF_ROLE_ID in [role.id for role in interaction.user.roles]):
            embedticketsetup = discord.Embed(title="ticket setup🎫", color=discord.Color.yellow())
            embedticketsetup.add_field(name="Setup", value="Setup the ticket by clicking the button below", inline=False)
            embedticketsetup.add_field(name="Create button", value="The create button is used to create the ticket panel", inline=False)
            embedticketsetup.add_field(name="Cancel button", value="The Cancel button is used to cancel the action", inline=False)
            embedticketsetup.set_footer(icon_url=ICONACROM, text="Powered by Acrom")
            embedticketsetup.set_thumbnail(url=ICONACROM)
            await interaction.response.send_message(embed=embedticketsetup, view=TicketButtonSetup(), ephemeral=True)
        else:
            embedticketerror = discord.Embed(title="ticket-setup Error", color=discord.Color.red())
            embedticketerror.add_field(name="Error", value="Non hai il permesso (administrator) per eseguire questo comando", inline=False)
            embedticketerror.set_footer(icon_url=ICONACROM, text="Powered by Acrom")
            embedticketerror.set_thumbnail(url=ICONACROM)
            await interaction.response.send_message(embed=embedticketerror, ephemeral=True)
