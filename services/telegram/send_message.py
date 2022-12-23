import telegram
from django.conf import settings


def send_message(text: str, chat_id: str) -> None:
    telegram_token = settings.TELEGRAM_TOKEN
    _bot = telegram.Bot(token=telegram_token)
    _bot.sendMessage(chat_id=chat_id, text=text, parse_mode=telegram.ParseMode.HTML)
