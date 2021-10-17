import logging
import token
from uuid import uuid4

from telegram import InlineQueryResultArticle, ParseMode, InputTextMessageContent, Update, InlineKeyboardButton, \
    InlineKeyboardMarkup, Bot
from telegram.ext import Updater, InlineQueryHandler, CommandHandler, CallbackContext
from telegram.utils.helpers import escape_markdown

# Enable logging
from MongoDBAPI.MongoDBAPI import Mongod
from TgBotAPI.config import BOT_TOKEN

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update: Update, context: CallbackContext) -> None:

    keyboard = [
        [
            InlineKeyboardButton("Последние новости", callback_data='last_tasks'),
            InlineKeyboardButton("Остановить бота", callback_data='stop_bot'),
        ],
        [InlineKeyboardButton("Подписаться на рассылку", callback_data='subscribe')],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text('Добро пожаловать!\nЭтот бот поможет Вам всегда оставаться в курсе событий.\n'
                              'Для продолжения работы выберите один из пунктов меню. При выборе пункта "Подписаться'
                              'на рассылку" бот в автоматическом режиме будет присылать Вам информацию с habr.com',
                              reply_markup=reply_markup)


def callback_start_menu(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    mongod = Mongod()

    if query.data == 'last_tasks':
        last_tasks = mongod.get_last_task(limit=5)
        id = query.from_user.id
        query.edit_message_text(text=f"Последние новости для Вас, надеюсь они будут полезны")
        for task in last_tasks:
            Bot(token=BOT_TOKEN).send_message(chat_id=id, text=f'{task["date"]}\n'
                                                               f'{task["price"]}\n'
                                                               f'{task["url"]}')
    if query.data == 'stop_bot':
        query.edit_message_text(text=f"Эта кнопка ничего не делает ☹️")
    if query.data == 'subscribe':
        query.edit_message_text(text=f"Спасибо за подписку! Но эта кнопка ничего не делает 😅")


def help_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Используйте команду /start чтобы начать работу.")


def inlinequery(update: Update, context: CallbackContext) -> None:
    """Handle the inline query."""
    query = update.inline_query.query

    if query == "":
        return

    results = [
        InlineQueryResultArticle(
            id=str(uuid4()),
            title="Caps",
            input_message_content=InputTextMessageContent(query.upper()),
        ),
        InlineQueryResultArticle(
            id=str(uuid4()),
            title="Bold",
            input_message_content=InputTextMessageContent(
                f"*{escape_markdown(query)}*", parse_mode=ParseMode.MARKDOWN
            ),
        ),
        InlineQueryResultArticle(
            id=str(uuid4()),
            title="Italic",
            input_message_content=InputTextMessageContent(
                f"_{escape_markdown(query)}_", parse_mode=ParseMode.MARKDOWN
            ),
        ),
    ]

    update.inline_query.answer(results)