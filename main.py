from telegram.ext import Updater, CommandHandler, InlineQueryHandler, CallbackQueryHandler

from FreelanceHabr.FreelanceHabr import FreelanceHabr
from MongoDBAPI.MongoDBAPI import Mongod
from TgBotAPI.TgBotAPI import start, help_command, inlinequery, callback_start_menu
from TgBotAPI.config import BOT_TOKEN as token


def main():
    # habr = FreelanceHabr()
    # mongod = Mongod()
    #
    # tasks = habr.get_habr_tasks()
    # last_five_tasks = mongod.get_last_task(5)
    # for task in last_five_tasks:
    #     print(task['name'])

    updater = Updater(token)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    updater.dispatcher.add_handler(CallbackQueryHandler(callback_start_menu))
    dispatcher.add_handler(CommandHandler("help", help_command))

    # on non command i.e message - echo the message on Telegram
    dispatcher.add_handler(InlineQueryHandler(inlinequery))

    # Start the Bot
    updater.start_polling()

    # Block until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
