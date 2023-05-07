from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from api.models import *


async def choice_shift_keyboard():
    button = [
        [InlineKeyboardButton(
            text=shift.letter_designation,
            callback_data=shift.id
        )] async for shift in Shift.objects.all()
    ]
    return InlineKeyboardMarkup(button)


async def choice_shop_keyboard():
    button = [
        [InlineKeyboardButton(
            text=shop.name,
            callback_data=shop.id
        )] async for shop in Shop.objects.all()
    ]
    return InlineKeyboardMarkup(button)


async def choice_zone_keyboard(shop_id):
    button = [
        [InlineKeyboardButton(
            text=zone.name,
            callback_data=zone.id
        )] async for zone in Zone.objects.filter(shop_id=shop_id)
    ]
    return InlineKeyboardMarkup(button)


async def choice_position_keyboard():
    button = [
        [InlineKeyboardButton(
            text=pos.name,
            callback_data=pos.id
        )] async for pos in Position.objects.all()
    ]
    return InlineKeyboardMarkup(button)
