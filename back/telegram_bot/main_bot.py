import logging
import os
from typing import Dict

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

from asgiref.sync import sync_to_async
from api.models import *


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

TOKEN = os.getenv('BOT_TOKEN')
CHOOSING, TYPING_REPLY, TYPING_CHOICE = range(3)


reply_keyboard = [
    ["Имя", "Фамилия"],
    ["Отчество", "Смена"],
    ["Цех", "Участок"],
    ["Табельный номер"],
    ["Готово"],
]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)


def facts_to_str(user_data: Dict[str, str]) -> str:
    facts = [f"{key} - {value}" for key, value in user_data.items()]
    return "\n".join(facts).join(["\n", "\n"])


async def start(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
) -> None:
    telegram_user = update.effective_user
    user_telegram_id = telegram_user.id
    if user_exist := await CustomUser.objects.filter(
            telegram_id=user_telegram_id
    ).aexists():
        await update.message.reply_text(
            f"Здравствуйте, {telegram_user.first_name} "
            f"{telegram_user.last_name}!"
        )
    else:
        await update.message.reply_text(
            f"Здравствуйте, {telegram_user.first_name} "
            f"{telegram_user.last_name}! "
            f"Пройдите регистрацию."
        )


async def registration(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
) -> int:

    await update.message.reply_text(
        "Заполните поля для регистрации: ",
        reply_markup=markup
    )
    return CHOOSING


async def regular_choice(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
) -> int:

    text = update.message.text
    context.user_data["choice"] = text
    if text == "Имя":
        await update.message.reply_text("Введите Ваше имя:")
    elif text == "Фамилия":
        await update.message.reply_text("Введите Вашу фамилию:")
    elif text == "Отчество":
        await update.message.reply_text("Введите Ваше отчество:")
    elif text == "Смена":
        keyboard_shifts = [
            [shift.letter_designation async for shift in Shift.objects.all()]
        ]
        markup_shifts = ReplyKeyboardMarkup(
            keyboard_shifts,
            resize_keyboard=True,
            one_time_keyboard=True,
            input_field_placeholder="Не вводить данные!"
        )
        await update.message.reply_text(
            "Укажите Вашу смену:",
            reply_markup=markup_shifts
        )
    elif text == "Цех":
        keyboard_shops = [[shop.name] async for shop in Shop.objects.all()]
        markup_shifts = ReplyKeyboardMarkup(
            keyboard_shops,
            resize_keyboard=True,
            one_time_keyboard=True,
            input_field_placeholder="Не вводить данные!"
        )
        await update.message.reply_text(
            "Укажите Ваш цех:",
            reply_markup=markup_shifts
        )
    elif text == "Участок":
        shop_name = context.user_data['Цех']
        keyboard_zones = [
            [zone.name] async for zone in Zone.objects.filter(
                shop__name=shop_name
            )
        ]
        markup_zones = ReplyKeyboardMarkup(
            keyboard_zones,
            resize_keyboard=True,
            one_time_keyboard=True,
            input_field_placeholder="Не вводить данные!"
        )
        await update.message.reply_text(
            "Укажите Ваш участок:",
            reply_markup=markup_zones
        )
    elif text == "Табельный номер":
        await update.message.reply_text("Введите Ваш табельный номер:")

    # TODO: Необходимо добавить вариант с выбором грейда и должности,
    #  так же по хорошему необходимо разделить эти функции в разные файлы,
    #  клавиатуры в один файл а может и в директорию,  функции в другие

    return TYPING_REPLY


async def received_information(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
) -> int:
    user_data = context.user_data
    text = update.message.text
    category = user_data["choice"]
    user_data[category] = text
    del user_data["choice"]

    await update.message.reply_text(
        "Ваши данные:"
        f"{facts_to_str(user_data)}"
        "Если все верно, нажмите готово.",
        reply_markup=markup,
    )

    return CHOOSING


async def done(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
) -> int:

    user_data = context.user_data
    if "choice" in user_data:
        del user_data["choice"]

    await CustomUser.objects.acreate(
        first_name=user_data['Имя'],
        last_name=user_data['Фамилия'],
        patronymic=user_data['Отчество'],
        telegram_id=update.effective_user.id,
        employee_id=user_data['Табельный номер'],
        shift=await Shift.objects.aget(letter_designation=user_data['Смена']),
        shop=await Shop.objects.aget(name=user_data['Цех']),
        zone=await Zone.objects.aget(name=user_data['Участок'])
    )

    await update.message.reply_text(
        f"Эти данные занесены в базу данных {facts_to_str(user_data)}",
        reply_markup=ReplyKeyboardRemove(),
    )

    user_data.clear()
    return ConversationHandler.END


def main() -> None:
    application = Application.builder().token(TOKEN).build()
    registration_dialog = ConversationHandler(
        entry_points=[CommandHandler('registration', registration)],
        states={
            CHOOSING: [
                MessageHandler(
                    filters.Regex(
                        "^(Имя|Фамилия|Отчество|Смена|Цех|Участок|Табельный номер)$"
                    ),
                    regular_choice,
                )
            ],
            TYPING_REPLY: [
                MessageHandler(
                    filters.TEXT & ~(filters.COMMAND | filters.Regex("^Готово$")),
                    received_information,
                )
            ],
        },
        fallbacks=[MessageHandler(filters.Regex("^Готово$"), done)],
    )
    application.add_handler(CommandHandler("start", start))
    application.add_handler(registration_dialog)
    application.run_polling()
