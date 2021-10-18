import logging
import token
from uuid import uuid4
from telegram import InlineQueryResultArticle, ParseMode, InputTextMessageContent, Update, InlineKeyboardButton, \
    InlineKeyboardMarkup, Bot
from telegram.ext import Updater, InlineQueryHandler, CommandHandler, CallbackContext
from telegram.utils.helpers import escape_markdown
from MongoDBAPI.MongoDBAPI import Mongod
from TgBotAPI.Keyboards.default_keyboards import Keyboards

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


def start(update: Update, context: CallbackContext) -> None:

    reply_markup = InlineKeyboardMarkup(Keyboards.start_menu())

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
            description = task["description"]
            if len(description) > 300:
                description = description[:300] + '...'
            message = f'Название: {task["name"]}\n' \
                      f'Дата размещения: {task["date"]}\n' \
                      f'Описание: {description}\n' \
                      f'Цена: {task["price"]}\n' \
                      f'Просмотры: {task["views"]}\n' \
                      f'Откликнулось: {task["responses"]}\n' \
                      f'Ссылка на задание: {task["url"]}\n'

            context.bot.send_message(chat_id=id, text=message, disable_web_page_preview=True, parse_mode='HTML')

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