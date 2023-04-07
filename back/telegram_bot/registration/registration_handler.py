from telegram import ReplyKeyboardRemove, Update, InlineKeyboardMarkup, \
    InlineKeyboardButton
from telegram.ext import (
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

from api.models import *
from telegram_bot.utils import facts_to_str
from .keyboards import (
    main_choice_keyboard,
    choice_shop_keyboard,
    choice_shift_keyboard,
    choice_zone_keyboard,
    choice_position_keyboard
)


CHOOSING, TYPING_REPLY, TYPING_CHOICE = range(3)


async def registration(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
) -> int:

    await update.message.reply_text(
        "Заполните поля для регистрации:",
        reply_markup=main_choice_keyboard()
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
    buttons = [
        InlineKeyboardButton(str(i), callback_data=str(i))
        for i in range(10)
    ]
    keyboard = InlineKeyboardMarkup([buttons])
    await update.message.reply_text(
        "Введите Ваш табельный номер:",
        reply_markup=keyboard
    )


async def handle_shift(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
) -> None:
    await update.message.reply_text(
        "Укажите Вашу смену:",
        reply_markup=choice_shift_keyboard()
    )


async def handle_shop(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
) -> None:
    await update.message.reply_text(
        "Укажите Ваш цех:",
        reply_markup=choice_shop_keyboard()
    )


async def handle_zone(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
) -> None:
    shop_name = context.user_data['Цех']
    await update.message.reply_text(
        "Укажите Ваш участок:",
        reply_markup=choice_zone_keyboard(shop_name)
    )


async def handle_position(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
) -> None:
    await update.message.reply_text(
        "Укажите Вашу должность:",
        reply_markup=choice_position_keyboard()
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
        reply_markup=main_choice_keyboard(),
    )

    return CHOOSING


async def create_user(
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
    fallbacks=[MessageHandler(filters.Regex("^Готово$"), create_user)],
)
