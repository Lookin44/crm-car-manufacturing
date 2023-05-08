from uuid import uuid4
from pathlib import Path

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

from .keyboards import (
    choice_shift_keyboard,
    choice_shop_keyboard,
    choice_zone_keyboard,
    choice_position_keyboard,
    data_keyboard
)
from telegram_bot.state_list import *


text_launch = {
    NAME:
        {
            'text': 'Укажите Вашу фамилию:',
            'exit_point': LAST_NAME,
        },
    LAST_NAME:
        {
            'text': 'Укажите Ваше отчество:',
            'exit_point': PATRONYMIC,
        },
    PATRONYMIC:
        {
            'text': 'Укажите Ваш табельный номер:',
            'exit_point': EMPLOYEE_ID,
        },
    EMPLOYEE_ID:
        {
            'text': 'Сделайте свое селфи',
            'exit_point': PHOTO,
        },
    PHOTO:
        {
            'text': 'Укажите Вашу смену:',
            'exit_point': SHIFT,
        },
    SHIFT:
        {
            'text': 'Укажите Вашу должность:',
            'exit_point': POSITION,
            'keyboard': choice_position_keyboard,
        },
    POSITION:
        {
            'text': 'Укажите Ваш цех:',
            'exit_point': SHOP,
            'keyboard': choice_shop_keyboard,
        },
    SHOP:
        {
            'text': 'Укажите Ваш участок',
            'exit_point': ZONE,
            'keyboard': choice_zone_keyboard,
        },
    ZONE:
        {
            'text': 'Верны ли следующие данные:',
            'exit_point': CHOOSE_EDIT_INFO,
            'keyboard': data_keyboard,
        },
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
    exit_point = text_launch.get(current_state).get('exit_point')

    user_data[current_state] = update.message.text

    await update.message.reply_text(message_text)

    user_data['current_state'] = exit_point
    return exit_point


async def photo_save(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data = context.user_data
    current_state = user_data.get('current_state')
    message_text = text_launch.get(current_state).get('text')
    exit_point = text_launch.get(current_state).get('exit_point')

    photo_file = await update.message.photo[-1].get_file()
    file_name = f'{uuid4()}.jpg'
    temp_path = Path.cwd() / 'telegram_bot' / 'registration' / 'temp_media'
    await photo_file.download_to_drive(custom_path=str(temp_path/file_name))
    await update.message.reply_text(
        message_text,
        reply_markup=await choice_shift_keyboard()
    )

    user_data['current_state'] = exit_point
    return exit_point


async def choose_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data = context.user_data
    current_state = user_data.get('current_state')
    message_text = text_launch.get(current_state).get('text')
    exit_point = text_launch.get(current_state).get('exit_point')
    keyboard = text_launch.get(current_state).get('keyboard')

    user_data[current_state] = update.callback_query.data

    await update.callback_query.answer()
    if current_state == SHOP:
        await update.callback_query.edit_message_text(
            message_text,
            reply_markup=await keyboard(user_data.get(current_state))
        )
    elif current_state == ZONE:
        await update.callback_query.edit_message_text(
            message_text,
            reply_markup=keyboard(context)
        )
    else:
        await update.callback_query.edit_message_text(
            message_text,
            reply_markup=await keyboard()
        )
    user_data['current_state'] = exit_point
    return exit_point


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
        SHIFT: [CallbackQueryHandler(choose_answer)],
        POSITION: [CallbackQueryHandler(choose_answer)],
        SHOP: [CallbackQueryHandler(choose_answer)],
        ZONE: [CallbackQueryHandler(choose_answer)],
    },
    fallbacks=[CallbackQueryHandler(done, pattern="^" + str(END) + "$")],
    map_to_parent={
        END: CHOOSE_ACTION,
    }
)
