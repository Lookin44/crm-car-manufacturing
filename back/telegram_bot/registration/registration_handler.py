from uuid import uuid4

from telegram import (
    ReplyKeyboardRemove,
    Update,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)
from telegram.ext import (
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters, CallbackQueryHandler,
)

from api.models import *
from telegram_bot.utils import facts_to_str
from .keyboards import (
    choice_shift_keyboard,
)
from telegram_bot.state_list import *


text_launch = {
    NAME: {'text': 'Укажите Вашу фамилию:', 'exit_point': LAST_NAME},
    LAST_NAME: {'text': 'Укажите Ваше отчество:', 'exit_point': PATRONYMIC},
    PATRONYMIC: {'text': 'Укажите Ваш табельный номер:', 'exit_point': EMPLOYEE_ID},
    EMPLOYEE_ID: {'text': 'Сделайте свое селфи', 'exit_point': PHOTO},
    PHOTO: {'text': 'Укажите Вашу смену:', 'exit_point': SHIFT},
    SHIFT: {'text': 'Укажите Вашу должность:', 'exit_point': POSITION},
    POSITION: {'text': 'Укажите Ваш цех:', 'exit_point': SHOP},
    SHOP: {'text': 'Укажите Ваш участок', 'exit_point': ZONE},
    ZONE: {'text': 'Сделайте свое селфи', 'exit_point': CHOOSE_EDIT_INFO},
}


async def start_reg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['current_state'] = NAME
    await update.callback_query.answer()
    await update.callback_query.edit_message_text('Укажите Ваше имя:')
    return NAME


async def typing_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data = context.user_data
    current_state = user_data.get('current_state')
    message_text = text_launch.get(current_state).get('text')

    user_data[current_state] = update.message.text

    await update.message.reply_text(message_text)

    exit_point = text_launch.get(current_state).get('exit_point')
    user_data['current_state'] = exit_point
    return exit_point


async def photo_save(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data = context.user_data
    current_state = user_data.get('current_state')
    message_text = text_launch.get(current_state).get('text')

    photo_file = await update.message.photo[-1].get_file()
    file_name = f'{uuid4()}.jpg'
    await photo_file.download_to_drive(file_name)
    await update.message.reply_text(message_text, reply_markup=await choice_shift_keyboard())

    exit_point = text_launch.get(current_state).get('exit_point')
    user_data['current_state'] = exit_point
    return exit_point


async def shift(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data = context.user_data
    current_state = user_data.get('current_state')
    message_text = text_launch.get(current_state).get('text')

    print(update.callback_query.data)

    await update.callback_query.answer()
    await update.callback_query.edit_message_text(message_text)


async def done(update: Update, context: ContextTypes.DEFAULT_TYPE):
    from telegram_bot.start.start_handler import start
    context.user_data['START_OVER'] = True
    await start(update, context)
    return END


registration_handler = ConversationHandler(
    entry_points=[CallbackQueryHandler(start_reg)],
    states={
        NAME:
            [MessageHandler(filters.TEXT & ~filters.COMMAND, typing_answer)],
        LAST_NAME:
            [MessageHandler(filters.TEXT & ~filters.COMMAND, typing_answer)],
        PATRONYMIC:
            [MessageHandler(filters.TEXT & ~filters.COMMAND, typing_answer)],
        EMPLOYEE_ID:
            [MessageHandler(filters.TEXT & ~filters.COMMAND, typing_answer)],
        PHOTO: [MessageHandler(filters.PHOTO & ~filters.COMMAND, photo_save)],
        SHIFT: [CallbackQueryHandler(shift)]
    },
    fallbacks=[CallbackQueryHandler(done, pattern="^" + str(END) + "$")],
    map_to_parent={
        END: CHOOSE_ACTION,
    }
)
