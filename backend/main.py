import json
import requests

from bson.objectid import ObjectId

from flask import Flask, request, session, jsonify
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_session import Session

from database import DatabaseHandler
from functions import QuestionProcessing
from config import Configuration, AppConfig

from telegram_handler import *
from vk_handler import *


app = Flask(__name__)
app.config.from_object(AppConfig)
bcrypt = Bcrypt(app)
cors = CORS(app, supports_credentials=True)
server_session = Session(app)


cfg = Configuration()
db = DatabaseHandler('help_desk_database', cfg.DB_URI)
qp = QuestionProcessing()


# set up webhook for Telegram
def set_telegram_webhook():
    url = f"https://api.telegram.org/bot{cfg.TELEGRAM_TOKEN}/setWebhook?url={cfg.SERVER_URL}/webhook/telegram"
    response = requests.post(
        url
    )
    if response.status_code == 200:
        print("Telegram webhook set successfully")
    else:
        print(response.json())
        print("Failed to set Telegram webhook")


with app.app_context():
    set_telegram_webhook()


# add routes for webhook handlers
@app.route('/webhook/telegram', methods=['POST'])
def handle_telegram_webhook():
    sn_id = db.social_network_exists('telegram')

    if sn_id is None:
        sn_id = db.insert_social_network('telegram')

    if 'message' in request.json.keys():
        request_data = request.json['message']
        chat_id = request_data["chat"]["id"]
        username = request_data["chat"]["username"]
        received_message = request_data['text']
        current_user = db.find_user(sn_id, chat_id)

        if not db.find_user(sn_id, chat_id):
            db.insert_user(sn_id, chat_id, received_message, username=username)
            current_user = db.find_user(sn_id, chat_id)

        db.update_user_last_message(current_user['_id'], received_message)
        all_questions = db.get_all_questions()
        closest_question = qp.find_closest_question(received_message, all_questions)

        if closest_question:
            qa = db.find_qna(closest_question)
            keyboard = {
                "inline_keyboard": [
                    [
                        {"text": "Да", "callback_data": "yes_nice"},
                        {"text": "Нет", "callback_data": "no_bad"}
                    ]
                ]
            }
            send_message_tg(chat_id, qa['answer'] + "\n\nЯ ответил на Ваш вопрос?", keyboard=keyboard)
        else:
            send_dont_know_message_tg(chat_id, "Я не знаю что ответить:(")
    
    elif 'callback_query' in request.json.keys():
        reply_data = request.json['callback_query']
        reply_answer = reply_data['data']
        user_id = reply_data['from']['id']
        current_user = db.find_user(sn_id, user_id)

        if 'nice' in reply_answer:
            send_message_tg(user_id, "Если чем-то еще могу помочь, спрашивайте!")
            return 'ok'
        elif 'bad' in reply_answer:
            if 'no' in reply_answer:
                send_dont_know_message_tg(user_id, "Жаль, что ответ Вам не подходит:(")
            else:
                send_message_tg(user_id, "Ваш вопрос перенаправлен службе поддержки.\nВам ответ первый освободившийся оператор.\nМогу я еще чем-то Вам помочь?")
                db.insert_request(
                    current_user['_id'],
                    sn_id,
                    user_id,
                    current_user['last_message']
                )
            return 'ok'

    return 'ok'


@app.route('/webhook/vk', methods=['POST'])
def handle_vk_webhook():
    sn_id = db.social_network_exists('vk')

    if sn_id is None:
        sn_id = db.insert_social_network('vk')
    data = request.json

    if data['type'] == 'confirmation':
        return cfg.VK_CONFIRMATION_CODE

    if data['type'] == 'message_new':
        message_data = data['object']['message']
        peer_id = message_data['peer_id']
        user_id = message_data['from_id']
        received_message = message_data['text']
        current_user = db.find_user(sn_id, user_id)

        if not current_user:
            db.insert_user(sn_id, user_id, received_message)
            current_user = db.find_user(sn_id, user_id)

        if 'payload' in message_data.keys():
            button_data = dict(json.loads(message_data['payload']))
            if 'nice' in button_data['button']:
                send_message_vk(peer_id, "Если чем-то еще могу помочь, спрашивайте!")
                return 'ok'
            elif 'bad' in button_data['button']:
                if 'no' in button_data['button']:
                    send_dont_know_message_vk(peer_id, "Жаль, что ответ Вам не подходит:(")
                else:
                    send_message_vk(peer_id, "Ваш вопрос перенаправлен службе поддержки.\nВам ответ первый освободившийся оператор.\nМогу я еще чем-то Вам помочь?")
                    db.insert_request(
                        current_user['_id'],
                        sn_id,
                        user_id,
                        current_user['last_message']
                    )
                    return 'ok'
            
        db.update_user_last_message(current_user['_id'], received_message)
        all_questions = db.get_all_questions()
        closest_question = qp.find_closest_question(received_message, all_questions)
        
        if closest_question:
            qa = db.find_qna(closest_question)
            keyboard = {
                "inline": True,
                "buttons": [
                    [{
                        "action": {
                            "type": "text",
                            "payload": "{\"button\": \"yes_nice\"}",
                            "label": "Да"
                        },
                        "color": "default"
                    }, {
                        "action": {
                            "type": "text",
                            "payload": "{\"button\": \"no_bad\"}",
                            "label": "Нет"
                        },
                        "color": "default"
                    }]
                ]
            }
            send_message_vk(peer_id, qa['answer'] + "\n\nЯ ответил на Ваш вопрос?", keyboard=keyboard)
        else:
            send_dont_know_message_vk(peer_id, "Я не знаю что ответить:(")

    return 'ok'


@app.route('/@me')
def get_current_user():
    user_id = session.get('operator_id')
    user = db.get_operator_by_id(ObjectId(user_id))
    data = {
        'code': "200"
    }
    if not user_id or user is None:
        data['code'] = "401"
    else:
        data['username'] = user['username']
    
    return jsonify(data)


@app.route('/register', methods=['POST'])
def register():
    username = request.json['username']
    password = request.json['password']

    if db.get_operator(username):
        return jsonify(
            {
                'error': 'Username already exists'
            }
        ), 409
    
    hashed_password = bcrypt.generate_password_hash(password)

    new_operator_id = str(db.insert_operator(username=username, password=hashed_password))

    session['operator_id'] = new_operator_id

    return jsonify(
        {
            'id': new_operator_id,
            'username': username
        }
    )


@app.route('/login', methods=['POST'])
def login():
    username = request.json['credentials']
    password = request.json['password']

    if username and password:
        operator = db.get_operator(username)

        if operator is None or not bcrypt.check_password_hash(operator['password'], password):
            return jsonify({'error': 'Bad credentials'}), 401

        session['operator_id'] = str(operator['_id'])
        print(session)

        return jsonify(
            {
                'id': str(operator['_id']),
                'username': operator['username']
            }
        )
    
    return jsonify(
        {'error': 'No data'}
    ), 410


@app.route('/logout', methods=['POST'])
def logout():
    session.pop('operator_id')
    return '200'


@app.route('/questions', methods=['GET'])
def message_handler():
    all_questions = db.get_all_requests()
    for question in all_questions:
        question['_id'] = str(question['_id'])
        question['sn_id'] = db.get_social_network_name(question['sn_id'])
        question['user_id'] = str(question['user_id'])
    return jsonify({'responses': all_questions})
    

@app.route('/send_answer', methods=['POST'])
def send_answer():
    response = request.json['response']
    db.update_request_status(ObjectId(response['_id']), "ended", response['user_answer'], response['operator'])
    sn = response['sn_id']
    if sn == 'vk':
        send_message_vk(response['user_chat_id'], f"Ваш вопрос:\n{response['user_question']}\nОтвет оператора:\n{response['user_answer']}")
    elif sn == 'telegram':
        send_message_tg(response['user_chat_id'], f"Ваш вопрос:\n{response['user_question']}\nОтвет оператора:\n{response['user_answer']}")
    return 'ok'


@app.route('/get_info', methods=['GET'])
def get_info():
    return jsonify({'info': "that's good"})


def run_app():
    db.insert_qna('qa.csv')
    app.run(debug=True)


if __name__ == '__main__':
    run_app()
