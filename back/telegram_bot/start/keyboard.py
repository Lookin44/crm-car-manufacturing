from telegram import InlineKeyboardButton

from telegram_bot.state_list import *


greeting_buttons = [
    [
        InlineKeyboardButton(
            text="Регистрация", callback_data=str(ADD_MYSELF)
        ),
        InlineKeyboardButton(
            text="Простой",
            callback_data=str(END)
        )
    ],
    [InlineKeyboardButton(text="Конец смены", callback_data=str(END))]
]

confirm_buttons = [
    [
        InlineKeyboardButton(text='✅Да', callback_data=str(CONFIRM)),
        InlineKeyboardButton(text='🚫Нет', callback_data=str(DISAGREE)),
    ]
]
