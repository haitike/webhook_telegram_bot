from __future__ import absolute_import
from gettext import gettext as _
import sys
import logging
import pytz
from datetime import datetime
from telegram import Updater
from telegram.error import TelegramError
from pytz import timezone, utc
from dungeon_world.database import Database

try:
    import configparser  # Python 3
except ImportError:
    import ConfigParser as configparser  # Python 2

CONFIGFILE_PATH = "data/config.cfg"
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("bot_log")

def translation_install(translation): # Comnpability with both python 2 / 3
    kwargs = {}
    if sys.version < '3':
        kwargs['unicode'] = True
    translation.install(**kwargs)

class Bot(object):
    translations = {}
    bot = None

    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read( CONFIGFILE_PATH )
        self.db = Database(self.config.get("dungeon_world","MONGO_URL"), self.config.get("dungeon_world","DB_NAME"))

        #self.db.create_index("user_data", "user_id") # REMEMBER TO ADD INDEXES FOR SPEED
        # i18n BLOCK (See haibot) / add system locale identification) / import gettext, os / config.cfg language, localedir / command_language

        self.updater = Updater(token=self.config.get("dungeon_world","TOKEN"))
        self.dispatcher = self.updater.dispatcher
        self.add_handlers()

        try:
            self.tzinfo = timezone(self.config.get("dungeon_world","TIMEZONE"))
        except:
            self.tzinfo = pytz.utc

    def start_polling_loop(self):
        self.disable_webhook()
        self.update_queue = self.updater.start_polling()
        self.updater.idle()
        self.cleaning()

    def start_webhook_server(self):
        self.set_webhook()
        self.update_queue = self.updater.start_webhook(self.config.get("dungeon_world","IP"),
                                                       self.config.getint("dungeon_world","PORT"),
                                                       self.config.get("dungeon_world","TOKEN"))
        self.updater.idle()
        self.cleaning()

    def cleaning(self):
        logger.info("Finished program.")

    def set_webhook(self):
        s = self.updater.bot.setWebhook(self.config.get("dungeon_world","WEBHOOK_URL") + "/" + self.config.get("dungeon_world","TOKEN"))
        if s:
            logger.info("webhook setup worked")
        else:
            logger.warning("webhook setup failed")
        return s

    def disable_webhook(self):
        s = self.updater.bot.setWebhook("")
        if s:
            logger.info("webhook was disabled")
        else:
            logger.warning("webhook couldn't be disabled")
        return s

    def add_handlers(self):
        self.dispatcher.addTelegramCommandHandler("start", self.command_start)
        self.dispatcher.addTelegramCommandHandler("help", self.command_help)
        self.dispatcher.addTelegramCommandHandler("time", self.command_time)
        self.dispatcher.addTelegramMessageHandler(self.command_echo)
        #self.dispatcher.addUnknownTelegramCommandHandler(self.command_unknown)
        #self.dispatcher.addErrorHandler(self.error_handle)

    def command_start(self, bot, update):
        self.send_message(bot, update.message.chat, _("Welcome to Dungeon World Bot."))

    def command_help(self, bot, update):
        self.send_message(bot, update.message.chat, _(
            """Available Commands:
            /start - Iniciciate or Restart the bot
            /help - Show the command list.
            /time - Bot local time check"""))

    def command_time(self, bot , update):
        utc_date = datetime.utcnow()
        local_date = pytz.utc.localize(utc_date).astimezone(self.tzinfo)
        formated_string = local_date.strftime("%d/%m/%y %H:%M")
        self.send_message(bot, update.message.chat, formated_string)

    def command_echo(self, bot , update):
        self.send_message(bot, update.message.chat, update.message.text)

    def send_message(self, bot, chat, text):
        try:
            bot.sendMessage(chat_id=chat.id, text=text)
            return True
        except TelegramError as e:
            logger.warning("Message sending error to %s [%d] [%s] (TelegramError: %s)" % (chat.name, chat.id, chat.type, e))
            return False
        except:
            logger.warning("Message sending error to %s [%d] [%s]" % (chat.name, chat.id, chat.type))
            return False
