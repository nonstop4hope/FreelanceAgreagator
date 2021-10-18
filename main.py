from telegram.ext import Updater, CommandHandler, InlineQueryHandler, CallbackQueryHandler

from FreelanceHabr.FreelanceHabr import FreelanceHabr
from MongoDBAPI.MongoDBAPI import Mongod
from TgBotAPI.TgBotAPI import start, help_command, inlinequery, callback_start_menu
from TgBotAPI.config import BOT_TOKEN as token


def main():
    habr = FreelanceHabr()
    habr.get_habr_tasks()

    updater = Updater(token)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    updater.dispatcher.add_handler(CallbackQueryHandler(callback_start_menu))
    dispatcher.add_handler(CommandHandler("help", help_command))

    dispatcher.add_handler(InlineQueryHandler(inlinequery))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
