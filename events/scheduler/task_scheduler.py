from apscheduler.schedulers.background import BackgroundScheduler
from utils.library.libs import *
from utils.func_utils import pulisci_dati_voti

scheduler = BackgroundScheduler()

def start_scheduler():
    scheduler.add_job(pulisci_dati_voti, 'interval', hours=12, id='pulisci_dati_voti')
    scheduler.start()
