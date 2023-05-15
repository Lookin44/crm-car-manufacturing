from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from api.models import *
from telegram_bot.state_list import *


async def choice_shift_keyboard():
    button = [
        [InlineKeyboardButton(
            text=shift.letter_designation,
            callback_data=shift.letter_designation
        )] async for shift in Shift.objects.all()
    ]
    return InlineKeyboardMarkup(button)


async def choice_shop_keyboard():
    button = [
        [InlineKeyboardButton(
            text=shop.name,
            callback_data=shop.name
        )] async for shop in Shop.objects.all()
    ]
    return InlineKeyboardMarkup(button)


async def choice_zone_keyboard(shop_name):
    button = [
        [InlineKeyboardButton(
            text=zone.name,
            callback_data=zone.name
        )] async for zone in Zone.objects.filter(shop__name=shop_name)
    ]
    return InlineKeyboardMarkup(button)


async def choice_position_keyboard():
    button = [
        [InlineKeyboardButton(
            text=pos.name,
            callback_data=pos.name
        )] async for pos in Position.objects.all()
    ]
    return InlineKeyboardMarkup(button)


def data_keyboard(context: ContextTypes.DEFAULT_TYPE):
    user_data = context.user_data
    user_name = InlineKeyboardButton(
        text=user_data.get(NAME), callback_data=NAME
    )
    user_last_name = InlineKeyboardButton(
        text=user_data.get(LAST_NAME), callback_data=LAST_NAME
    )
    user_patronymic = InlineKeyboardButton(
        text=user_data.get(PATRONYMIC), callback_data=PATRONYMIC
    )
    user_employee_id = InlineKeyboardButton(
        text=user_data.get(EMPLOYEE_ID), callback_data=EMPLOYEE_ID
    )
    user_shift = InlineKeyboardButton(
        text=user_data.get(SHIFT), callback_data=POSITION
    )
    user_position = InlineKeyboardButton(
        text=user_data.get(POSITION), callback_data=SHIFT
    )
    user_shop = InlineKeyboardButton(
        text=user_data.get(SHOP), callback_data=SHOP
    )
    user_zone = InlineKeyboardButton(
        text=user_data.get(ZONE), callback_data=ZONE
    )
    done = InlineKeyboardButton(
        text='✅ Все верно ✅', callback_data=END
    )
    button = [
        [user_name, user_last_name, user_patronymic],
        [user_employee_id, user_position],
        [user_shift, user_shop, user_zone],
        [done]
    ]
    return InlineKeyboardMarkup(button)
