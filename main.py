import telebot
import requests
from telebot import types
import os

# --- KUTUBXONALARNI TEKSHIRISH ---
try:
    from gtts import gTTS
    GTTS_AVAILABLE = True
except ImportError:
    GTTS_AVAILABLE = False

# --- SOZLAMALAR ---
# Tokeningizni bu yerga yozing
TOKEN = "8520252575:AAGxbYsmhH0ktk_Cy1nmWQUZbVcK-pOE440"
bot = telebot.TeleBot(TOKEN)

# --- START BUYRUG'I ---
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = types.KeyboardButton("💰 Valyuta")
    btn2 = types.KeyboardButton("🎙 Matnni ovoz qilish")
    btn3 = types.KeyboardButton("📲 QR Yaratish")
    btn4 = types.KeyboardButton("🖼 Rasm")
    btn5 = types.KeyboardButton("ℹ️ Ma'lumot")
    markup.add(btn1, btn2, btn3, btn4, btn5)
    
    bot.send_message(
        message.chat.id, 
        f"Salom {message.from_user.first_name}! Men Chiki chiki botman. Nima qilamiz?", 
        reply_markup=markup
    )

# 1. VALYUTA KURSI
@bot.message_handler(func=lambda m: m.text == "💰 Valyuta")
def get_currency(message):
    try:
        url = "https://cbu.uz/uz/arkhiv-kursov-valyut/json/"
        response = requests.get(url).json()
        usd = next(item for item in response if item['Ccy'] == 'USD')
        bot.send_message(message.chat.id, f"🇺🇸 1 Dollar = {usd['Rate']} so'm\n📅 Sana: {usd['Date']}")
    except:
        bot.send_message(message.chat.id, "Kursni yuklashda xatolik yuz berdi.")

# 2. MATNNI OVOZ QILISH (gTTS)
@bot.message_handler(func=lambda m: m.text == "🎙 Matnni ovoz qilish")
def voice_request(message):
    if not GTTS_AVAILABLE:
        bot.send_message(message.chat.id, "Kutubxona o'rnatilmagan. Pydroid Terminalda 'pip install gTTS' yozing.")
        return
    msg = bot.send_message(message.chat.id, "Ovozga aylantirish uchun matn yuboring (Masalan: Salom):")
    bot.register_next_step_handler(msg, process_voice)

def process_voice(message):
    try:
        tts = gTTS(text=message.text, lang='ru') # Rus yoki O'zbek tili uchun 'ru' mos keladi
        tts.save("voice.mp3")
        with open("voice.mp3", "rb") as audio:
            bot.send_voice(message.chat.id, audio)
        os.remove("voice.mp3")
    except Exception as e:
        bot.send_message(message.chat.id, "Xatolik yuz berdi. Matn yuborganingizga ishonch hosil qiling.")

# 3. QR KOD YARATISH
@bot.message_handler(func=lambda m: m.text == "📲 QR Yaratish")
def qr_request(message):
    msg = bot.send_message(message.chat.id, "QR kod ichiga nima yozay? (Link yoki so'z yuboring):")
    bot.register_next_step_handler(msg, process_qr)

def process_qr(message):
    qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size=250x250&data={message.text}"
    bot.send_photo(message.chat.id, qr_url, caption="Sizning QR kodingiz!")

# 4. TASODIFIY RASM
@bot.message_handler(func=lambda m: m.text == "🖼 Rasm")
def send_random_pic(message):
    pic_url = "https://picsum.photos/640/360"
    bot.send_photo(message.chat.id, pic_url, caption="Mana sizga rasm!")

# 5. INFO
@bot.message_handler(func=lambda m: m.text == "ℹ️ Ma'lumot")
def info(message):
    bot.send_message(message.chat.id, "Bot yaratuvchisi: Abdulhakim\nFunksiyalar: Valyuta, Ovoz, QR, Rasm.")

# --- BOTNI ISHGA TUSHIRISH ---
print("Bot muvaffaqiyatli yoqildi...")
bot.infinity_polling()
