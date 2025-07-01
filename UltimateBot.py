from utils.library.libs import *
from utils.func_utils import *


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