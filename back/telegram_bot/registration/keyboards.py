from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from api.models import *


async def choice_shift_keyboard():
    button = [
        [InlineKeyboardButton(text=shift.letter_designation, callback_data=shift.id)] async for shift in Shift.objects.all()
    ]
    return InlineKeyboardMarkup(button)


# async def choice_shop_keyboard():
#     return ReplyKeyboardMarkup(
#         [[shop.name] async for shop in Shop.objects.all()],
#         resize_keyboard=True,
#         one_time_keyboard=True,
#         input_field_placeholder="Не вводить данные!"
#     )
#
#
# async def choice_zone_keyboard(shop_name):
#     return ReplyKeyboardMarkup(
#         [[zone.name] async for zone in Zone.objects.filter(
#             shop__name=shop_name
#         )],
#         resize_keyboard=True,
#         one_time_keyboard=True,
#         input_field_placeholder="Не вводить данные!"
#     )
#
#
# async def choice_position_keyboard():
#     return ReplyKeyboardMarkup(
#         [[pos.name] async for pos in Position.objects.all()],
#         resize_keyboard=True,
#         one_time_keyboard=True,
#         input_field_placeholder="Не вводить данные!"
#     )
