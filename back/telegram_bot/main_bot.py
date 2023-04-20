import logging
import os

from telegram.ext import Application
from .start.start_handler import greeting_handler


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

TOKEN = os.getenv('BOT_TOKEN')


def main() -> None:
    application = Application.builder().token(TOKEN).build()
    application.add_handler(greeting_handler)
    application.run_polling()
