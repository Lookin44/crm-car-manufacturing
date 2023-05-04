from telegram import Update, InlineKeyboardMarkup
from telegram.ext import (
    ContextTypes,
    ConversationHandler,
    CommandHandler,
    CallbackQueryHandler
)

from api.models import *
from telegram_bot.utils import check_time
from telegram_bot.state_list import *
from telegram_bot.registration.registration_handler import registration_handler
from telegram_bot.start.keyboard import greeting_buttons, confirm_buttons


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = 'Выберите дальнейшее действие.'
    if context.user_data.get('START_OVER'):
        await update.callback_query.answer()
        await update.callback_query.edit_message_text(
            text=text,
            reply_markup=InlineKeyboardMarkup(greeting_buttons)
        )
    user = update.effective_user
    if await CustomUser.objects.filter(telegram_id=user.id).aexists():
        user_db = await CustomUser.objects.aget(telegram_id=user.id)
        await update.message.reply_text(
            f"{check_time()}, {user_db.first_name} {user_db.patronymic}!"
        )
    else:
        await update.message.reply_text(
            f"{check_time()}, {user.first_name} {user.last_name}! "
        )
        await update.message.reply_text(
            text=text,
            reply_markup=InlineKeyboardMarkup(greeting_buttons)
        )
    return CHOOSE_ACTION


async def add_myself(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = 'Вы готовы начать?'
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(
        text=text,
        reply_markup=InlineKeyboardMarkup(confirm_buttons)
    )
    return REGISTRATION


greeting_handler = ConversationHandler(
    entry_points=[CommandHandler('start', start)],
    states={
        CHOOSE_ACTION: [
            CallbackQueryHandler(
                add_myself,
                pattern="^" + str(ADD_MYSELF) + "$"),
        ],
        REGISTRATION: [registration_handler],
    },
    fallbacks=[],
)
