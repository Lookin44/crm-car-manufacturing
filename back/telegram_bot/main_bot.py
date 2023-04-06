import logging
import os

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

from api.models import *
from .utils import facts_to_str, check_time


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
    ["Должность"],
    ["Готово"],
]
markup = ReplyKeyboardMarkup(
    reply_keyboard,
    one_time_keyboard=True,
    input_field_placeholder="Не вводить данные!"
)


async def start(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
) -> None:
    telegram_user = update.effective_user
    user_telegram_id = telegram_user.id
    if user_exist := await CustomUser.objects.filter(
            telegram_id=user_telegram_id
    ).aexists():
        user = await CustomUser.objects.aget(telegram_id=user_telegram_id)
        await update.message.reply_text(
            f"{check_time()}, {user.first_name} "
            f"{user.patronymic}!"
        )
    else:
        await update.message.reply_text(
            f"{check_time()}, {telegram_user.first_name} "
            f"{telegram_user.last_name}! "
            f"Пройдите регистрацию. /registration"
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


async def handle_name(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
) -> None:
    await update.message.reply_text("Введите Ваше имя:")


async def handle_surname(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
) -> None:
    await update.message.reply_text("Введите Вашу фамилию:")


async def handle_patronymic(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
) -> None:
    await update.message.reply_text("Введите Ваше отчество:")


async def handle_employee_id(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
) -> None:
    await update.message.reply_text("Введите Ваш табельный номер:")


async def handle_shift(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
) -> None:
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


async def handle_shop(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
) -> None:
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


async def handle_zone(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
) -> None:
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


async def handle_position(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
) -> None:
    markup_shifts = ReplyKeyboardMarkup(
        [[pos.name] async for pos in Position.objects.all()],
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Не вводить данные!"
    )
    await update.message.reply_text(
        "Укажите Вашу должность:",
        reply_markup=markup_shifts
    )


async def regular_choice(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
) -> int:

    switcher = {
        "Имя": handle_name,
        "Фамилия": handle_surname,
        "Отчество": handle_patronymic,
        "Смена": handle_shift,
        "Цех": handle_shop,
        "Участок": handle_zone,
        "Табельный номер": handle_employee_id,
        "Должность": handle_position,
    }

    text = update.message.text
    context.user_data["choice"] = text

    if text in switcher:
        await switcher[text](update, context)
        return TYPING_REPLY
    else:
        await update.message.reply_text(
            "Я не понимаю, о чем Вы говорите. Попробуйте еще раз."
        )
        return CHOOSING


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
                        "^(Имя|Фамилия|Отчество|Смена|Цех|"
                        "Участок|Табельный номер|Должность)$"
                    ),
                    regular_choice,
                )
            ],
            TYPING_REPLY: [
                MessageHandler(
                    filters.TEXT & ~(
                            filters.COMMAND | filters.Regex("^Готово$")
                    ),
                    received_information,
                )
            ],
        },
        fallbacks=[MessageHandler(filters.Regex("^Готово$"), done)],
    )
    application.add_handler(CommandHandler("start", start))
    application.add_handler(registration_dialog)
    application.run_polling()
