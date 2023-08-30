import json
import requests

from config import Configuration
from database import DatabaseHandler


cfg = Configuration()
db = DatabaseHandler('help_desk_database', cfg.DB_URI)
TOKEN = cfg.TELEGRAM_TOKEN


def send_message_tg(chat_id: int, message: str, *args, **kwargs):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {"chat_id": chat_id, "text": message}
    if 'keyboard' in kwargs.keys():
        data['reply_markup'] = json.dumps(kwargs['keyboard'])
    print(data)
    response = requests.post(url, data=data)
    print(response.json())


def send_dont_know_message_tg(chat_id: int, message: str):
    keyboard = {
        "inline_keyboard": [
            [
                {"text": "Да", "callback_data": "yes_bad"},
                {"text": "Нет", "callback_data": "no_nice"}
            ]
        ]
    }
    message += "\nЖелаете, чтобы я перенаправил Ваш вопрос оператору?"
    send_message_tg(chat_id, message, keyboard=keyboard)