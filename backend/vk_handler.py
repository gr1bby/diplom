import json
import random
import requests

from config import Configuration
from database import DatabaseHandler


cfg = Configuration()
db = DatabaseHandler('help_desk_database', cfg.DB_URI)
TOKEN = cfg.VK_TOKEN
SECRET = cfg.VK_SECRET


def send_message_vk(user_id: int, message: str, *args, **kwargs):
    url = "https://api.vk.com/method/messages.send"
    params = {
        "user_id": user_id,
        "random_id": random.randint(0, 128),
        "secret_key": cfg.VK_SECRET,
        "access_token": cfg.VK_TOKEN,
        "v": "5.131",
        "message": message,
    }
    if 'keyboard' in kwargs.keys():
        params['keyboard'] = json.dumps(kwargs['keyboard'])
    response = requests.post(url, params=params)
    # print(response.json())


def send_dont_know_message_vk(user_id: int, message: str):
    keyboard = {
        "inline": True,
        "buttons": [
            [{
                "action": {
                    "type": "text",
                    "payload": "{\"button\": \"yes_bad\"}",
                    "label": "Да"
                },
                "color": "default"
            }, {
                "action": {
                    "type": "text",
                    "payload": "{\"button\": \"no_nice\"}",
                    "label": "Нет"
                },
                "color": "default"
            }]
        ]
    }
    message += "\nЖелаете, чтобы я перенаправил Ваш вопрос оператору?"
    send_message_vk(user_id, message, keyboard=keyboard)
