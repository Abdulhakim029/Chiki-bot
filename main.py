import telebot
import requests
import qrcode
import io
from flask import Flask
from threading import Thread

# --- 1. UYG'OQ SAQLASH UCHUN VEB SERVER (Render uchun) ---
app = Flask('')

@app.route('/')
def home():
    return "Bot uyg'oq va ishlamoqda!"

def run():
    # Render 10000 portini talab qiladi
    app.run(host='0.0.0.0', port=10000)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- 2. BOT SOZLAMALARI (Rasmdagi token qo'shildi) ---
BOT_TOKEN = "8520252575:AAGxbYsmhH0ktk_Cy1nmWQUZbVcK-p0E440"
bot = telebot.TeleBot(BOT_TOKEN)

# /start buyrug'i
@bot.message_handler(commands=['start'])
def start(message):
    welcome_text = (
        "Assalomu alaykum! Men aqlli @Chiki_029_bot man. 🤖\n\n"
        "Menga istalgan savolingizni bering, AI yordamida javob beraman!\n\n"
        "Menyu:\n"
        "💰 /currency - Valyuta kurslari\n"
        "📲 /qr [matn] - QR kod yaratish\n"
    )
    bot.send_message(message.chat.id, welcome_text)

# Valyuta kursi (NBU API orqali)
@bot.message_handler(commands=['currency'])
def get_currency(message):
    try:
        url = "https://nbu.uz/uz/exchange-rates/json/"
        res = requests.get(url).json()
        usd = next(item for item in res if item['code'] == 'USD')
        bot.send_message(message.chat.id, f"🇺🇿 MB kursi: 1 USD = {usd['cb_price']} so'm")
    except:
        bot.send_message(message.chat.id, "Kurs ma'lumotini olishda xatolik yuz berdi.")

# QR kod yaratish
@bot.message_handler(commands=['qr'])
def make_qr(message):
    data = message.text.replace('/qr', '').strip()
    if not data:
        bot.reply_to(message, "Iltimos, QR kod ichida nima bo'lishini yozing. Masalan: /qr Salom")
        return
    
    img = qrcode.make(data)
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    buf.seek(0)
    bot.send_photo(message.chat.id, buf)

# 🧠 SUN'IY INTELLEKT (Savol-javob qismi)
@bot.message_handler(func=lambda message: True)
def chat_with_ai(message):
    # Bot yozayotganini ko'rsatish
    bot.send_chat_action(message.chat.id, 'typing')
    
    try:
        # Bepul va kalit talab qilmaydigan AI xizmati
        url = f"https://api.simsimi.vn/v2/?text={message.text}&lc=uz"
        response = requests.get(url).json()
        ai_javob = response.get('result', "Kechirasiz, hozir javob bera olmayman.")
        bot.reply_to(message, ai_javob)
    except:
        bot.reply_to(message, "Ulanishda xatolik bo'ldi. Keyinroq urinib ko'ring.")

# --- 3. BOTNI ISHGA TUSHIRISH ---
if __name__ == "__main__":
    keep_alive() # Veb-serverni yoqish
    print("Bot ishga tushdi...")
    bot.polling(none_stop=True)
    
