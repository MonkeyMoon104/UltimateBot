import discord
from discord.ext import commands
from colorama import Fore
from dotenv import load_dotenv
import os
from utils.db_utils import *
from utils.func_utils import *
from utils.image_utils import *
from utils.bot_tasks import setup as setup_tasks
from events.scheduler.task_scheduler import start_scheduler
from events.join import handle_member_join
from commands.manager.group_register import groups
from data.config  import *
from utils.classes.views.ticket.buttons.general.close_claim_ticket_button import CloseClaimTicketButton
from utils.classes.views.ticket.buttons.setup.ticket_button_setup import TicketButtonSetup
from utils.classes.views.roleselection.role_selection_view import RoleSelectionView
from utils.classes.views.verification.verification_view import VerificationView
from utils.classes.views.ticket.select.ticket_select import TicketSelectView
from utils.classes.views.thread.buttons.close.close_button_thread import CloseButtonThread
from utils.classes.views.thread.buttons.delete.delete_button_view import DeleteButtonView
from utils.classes.views.qrcode.store.store_view import StoreView
from utils.classes.views.qrcode.voto.voto_view import VotoView
from utils.classes.views.qrcode.invite.invite_view import InviteView
from utils.classes.views.suggestion.suggestion_view import SuggestionButtons
from utils.classes.views.apply.availability_buttons import AvailabilityButtons
from utils.classes.views.apply.availability_notifier import AvailabilityNotifier


load_dotenv()
print("Caricando le variabili...")

print("Tutte le variabili sono state caricate procedo...")

crea_file_json_vuoto()

intents = discord.Intents.all()
intents.presences = False

client = commands.Bot(command_prefix="/", description="A multi-functions discord bot", intents=intents)

start_scheduler()

@client.event
async def on_ready():
    print(Fore.GREEN + "We have logged in as " + Fore.BLUE +  f"{client.user}")
    print(Fore.YELLOW + "------")

    setup_tasks(client)
    apply_init_db()
    print(Fore.GREEN + "Task entrate in funzione")
    print(Fore.YELLOW + "------")   

    for group in groups:
        client.tree.remove_command(group)

    print(Fore.GREEN + "Comandi " + Fore.RED + "(/)" + Fore.GREEN + " in caricamento")
    print(Fore.YELLOW + "------")

    for group in groups:
        client.tree.add_command(group)
    client.add_view(CloseClaimTicketButton())
    client.add_view(TicketButtonSetup())
    client.add_view(RoleSelectionView())
    client.add_view(VerificationView())
    client.add_view(TicketSelectView())
    client.add_view(CloseButtonThread())
    client.add_view(DeleteButtonView())
    client.add_view(StoreView())
    client.add_view(VotoView())
    client.add_view(InviteView())
    client.add_view(SuggestionButtons())
    client.add_view(AvailabilityButtons())

    AvailabilityNotifier(client)

    await load_commands(client)
    await load_context_menus(client)
    synced = await client.tree.sync()
    print(Fore.GREEN + "Comandi " + Fore.RED + "(/)" + Fore.GREEN + f" ricaricati e registrati: {len(synced)}")
    print(Fore.YELLOW + "------")

@client.event
async def on_member_join(member: discord.Member):
    await handle_member_join(member, client)

client.run(TOKEN)