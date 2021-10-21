from telegram.ext import Updater, CommandHandler, InlineQueryHandler, CallbackQueryHandler

from FreelanceHabr.FreelanceHabr import FreelanceHabr
from MongoDBAPI.MongoDBAPI import Mongod
from TgBotAPI.TgBotAPI import start, help_command, inlinequery, callback_start_menu
from TgBotAPI.config import BOT_TOKEN as token
import threading
from time import sleep


def main() -> None:
    habr = FreelanceHabr()
    while True:
        habr.get_habr_tasks()
        sleep(120)


if __name__ == '__main__':
    main()
