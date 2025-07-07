from flask import Flask, request
import telebot

API_TOKEN = 'TOKENINGNI_BUYERGA_YOZ'
bot = telebot.TeleBot(API_TOKEN)
app = Flask(__name__)

WEBHOOK_URL = f'https://SENING-RAILWAY-URLING/{API_TOKEN}'

@app.route('/' + API_TOKEN, methods=['POST'])
def get_message():
    json_str = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return '!', 200

# 🔻 **SENING SAVOLINGGA JAVOB: Bu qism shu yerda bo‘ladi**
@app.route("/", methods=['GET'])
def set_webhook():
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
