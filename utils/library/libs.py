import discord
import os
import requests
import json
import mysql.connector
import typing
import importlib
import asyncio
import sqlite3
import yt_dlp
import re
import pytz
import datetime
import qrcode
import validators
import io
from utils.db_utils import *
from utils.image_utils import *
from utils.bot_tasks import setup as setup_tasks
from events.scheduler.task_scheduler import start_scheduler
from events.join import handle_member_join
from commands.manager.group_register import groups
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
from utils.classes.views.apply.availability_modal import AvailabilityModal
from utils.classes.views.suggestion.link.suggestion_link import SuggestionLink
from utils.classes.views.ticket.link.channels_ticket_link import ChannelsTicketLink
from utils.classes.views.ticket.modal.ticket_info_modal import TicketInfoModal
from utils.classes.views.general.profile.profile_view_links import ProfileViewLinks
from discord.ext import commands
from discord import utils as Utils
from colorama import Fore
from dotenv import load_dotenv
from io import BytesIO
from PIL import Image, ImageFont, ImageDraw
from mcstatus import JavaServer
from collections import deque
from apscheduler.schedulers.background import BackgroundScheduler
from humanfriendly import parse_timespan, InvalidTimespan, format_timespan
from datetime import timedelta
from zoneinfo import ZoneInfo
