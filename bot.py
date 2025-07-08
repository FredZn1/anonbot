from flask import Flask, request
import telebot

app = Flask(__name__)

API_TOKEN = '7877469815:AAFGztBWQoACTgJl7j9hez8RkMyV7U4oo3M'
ADMIN_ID = 7721840289
bot = telebot.TeleBot(API_TOKEN)

# 🗂 Xotirada user_idlarni saqlash uchun dict
user_messages = {}

@app.route("/api/bot", methods=['POST'])
def webhook():
    json_str = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return '!', 200

@app.route("/", methods=['GET'])
def index():
    bot.remove_webhook()
    bot.set_webhook(url="https://anonbot-psi.vercel.app/api/bot")
    return "Webhook set!", 200

# 🔧 /start komandasi
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Здравствуйте! Напишите своё сообщение.")

# 🔧 Har qanday xabarni qabul qilish
@bot.message_handler(func=lambda message: True)
def handle_all(message):
    if message.from_user.id != ADMIN_ID:
        # Foydalanuvchi xabarini admin'ga forward qilish
        sent = bot.forward_message(ADMIN_ID, message.chat.id, message.message_id)
        # Forward qilingan xabar_id asosida user_id saqlash
        user_messages[sent.message_id] = message.chat.id
        # Foydalanuvchiga javob
        bot.reply_to(message, "Ваше сообщение отправлено, ожидайте ответа.")
    else:
        # Agar admin javob yozayotgan bo‘lsa
        if message.reply_to_message and message.reply_to_message.message_id in user_messages:
            user_id = user_messages[message.reply_to_message.message_id]
            bot.send_message(user_id, f"Ответ от админа:\n{message.text}")
        else:
            bot.send_message(ADMIN_ID, "Пожалуйста, отвечайте на пересланные сообщения, чтобы отправить ответ пользователю.")

# Vercel serverless function uchun handler
def handler(environ, start_response):
    return app(environ, start_response)
