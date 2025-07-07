from flask import Flask, request
import telebot

# 🔑 BOT TOKENING
API_TOKEN = '7877469815:AAFGztBWQoACTgJl7j9hez8RkMyV7U4oo3M'
bot = telebot.TeleBot(API_TOKEN)
app = Flask(__name__)

# 🔗 Railway URL + token
WEBHOOK_URL = f'https://anonbot.up.railway.app/{API_TOKEN}'

@app.route('/' + API_TOKEN, methods=['POST'])
def get_message():
    json_str = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return '!', 200

@app.route('/', methods=['GET'])
def index():
    bot.remove_webhook()
    bot.set_webhook(url=WEBHOOK_URL)
    return 'Webhook set!', 200

# 🔧 /start komandasi
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Здравствуйте! Напишите своё сообщение.")

# 🔧 Har qanday xabarga javob
@bot.message_handler(func=lambda message: True)
def handle_all(message):
    bot.reply_to(message, "Ваше сообщение отправлено, ожидайте ответа.")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
