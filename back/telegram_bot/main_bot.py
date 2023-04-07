import logging
import os

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
)

from api.models import *
from .registration.registration_handler import registration_dialog
from .utils import check_time


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

TOKEN = os.getenv('BOT_TOKEN')


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


def main() -> None:
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(registration_dialog)
    application.run_polling()
