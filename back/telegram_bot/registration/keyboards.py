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


async def data_keyboard(context: ContextTypes.DEFAULT_TYPE):
    user_data = context.user_data
    user_name = user_data.get(NAME)
    user_last_name = user_data.get(LAST_NAME)
    user_patronymic = user_data.get(PATRONYMIC)
    user_employee_id = user_data.get(EMPLOYEE_ID)
    user_shift = user_data.get(SHIFT)
    user_position = user_data.get(POSITION)
    user_shop = user_data.get(SHOP)
    user_zone = user_data.get(ZONE)
    button = [
        [
            InlineKeyboardButton(text=user_name, callback_data=NAME),
            InlineKeyboardButton(text=user_last_name, callback_data=LAST_NAME),
        ],
        [InlineKeyboardButton(text=user_patronymic, callback_data=PATRONYMIC),],
        [InlineKeyboardButton(text=user_employee_id, callback_data=EMPLOYEE_ID),],
        [InlineKeyboardButton(text=user_position, callback_data=POSITION),],
        [
            InlineKeyboardButton(text=user_shift, callback_data=SHIFT),
            InlineKeyboardButton(text=user_shop, callback_data=SHOP),
            InlineKeyboardButton(text=user_zone, callback_data=ZONE),
        ],
    ]
    return InlineKeyboardMarkup(button)
