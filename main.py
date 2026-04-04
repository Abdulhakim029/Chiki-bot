import telebot
import requests
import google.generativeai as genai
from gtts import gTTS
import qrcode
import io
import os
from flask import Flask
from threading import Thread

# --- UYG'OQ SAQLASH UCHUN VEB SERVER ---
app = Flask('')

@app.route('/')
def home():
    return "Men uyg'oqman!"

def run():
    app.run(host='0.0.0.0', port=10000)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- BOT SOZLAMALARI ---
BOT_TOKEN = "SIZNING_BOT_TOKENINGIZ" # O'zingizni tokeningizni yozing
AI_API_KEY = "SIZNING_GEMINI_API_KEYINGIZ" # AI Studio'dan olgan kalitingiz

# AI-ni sozlash
genai.configure(api_key=AI_API_KEY)
ai_model = genai.GenerativeModel('gemini-pro')

bot = telebot.TeleBot(BOT_TOKEN)

# /start buyrug'i
@bot.message_handler(commands=['start'])
def start(message):
    welcome_text = (
        "Assalomu alaykum! Men aqlli botman. 🤖\n\n"
        "Menga savol bering (AI javob beradi), yoki:\n"
        "/currency - Kurslar 💰\n"
        "/qr [matn] - QR kod 📲\n"
        "/voice [matn] - Ovozli xabar 🎙"
    )
    bot.send_message(message.chat.id, welcome_text)

# Valyuta kursi
@bot.message_handler(commands=['currency'])
def get_currency(message):
    url = "https://nbu.uz/uz/exchange-rates/json/"
    res = requests.get(url).json()
    usd = next(item for item in res if item['code'] == 'USD')
    text = f"🇺🇿 MB kursi: 1 USD = {usd['cb_price']} so'm"
    bot.send_message(message.chat.id, text)

# QR kod
@bot.message_handler(commands=['qr'])
def make_qr(message):
    data = message.text.replace('/qr', '').strip()
    if not data:
        bot.reply_to(message, "Matn yuboring: /qr salom")
        return
    img = qrcode.make(data)
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    buf.seek(0)
    bot.send_photo(message.chat.id, buf)

# Sun'iy intellekt
@bot.message_handler(func=lambda message: True)
def chat_with_ai(message):
    try:
        bot.send_chat_action(message.chat.id, 'typing')
        response = ai_model.generate_content(message.text)
        bot.reply_to(message, response.text)
    except:
        bot.reply_to(message, "Hozircha javob bera olmayman.")

# ASOSIY QISM
if __name__ == "__main__":
    keep_alive() # Veb-serverni ishga tushirish
    bot.polling(none_stop=True)
    
