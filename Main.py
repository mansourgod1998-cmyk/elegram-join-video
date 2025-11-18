import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import random
import string

\\# توکن ربات
TOKEN = \"8562651796:AAFj13lnnFffHLeeF_3POAkDN-Lm_Qt3pg4\"

\\# لیست کانال‌ها فعلاً خالیه، بعداً اضافه می‌کنی
CHANNELS = \\[\\]  # مثال: \\[\"@Channel1\", \"@Channel2\"\\]

bot = telebot.TeleBot(TOKEN)

\\# دیتابیس ساده در مموری
video_links = {}  # format: { \"link8حرف\": \"file_id\" }
user_status = {}

\\# تولید لینک اختصاصی برای هر فیلم
def generate_link():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=8))

\\# چک عضویت
def check_membership(user_id):
    not_joined = \\[\\]
    for ch in CHANNELS:
        try:
            member = bot.get_chat_member(ch, user_id)
            if member.status in \\[\"left\", \"kicked\"\\]:
                not_joined.append(ch)
        except:
            not_joined.append(ch)
    return not_joined

\\# دریافت فیلم از تو
@bot.message_handler(content_types=\\['video'\\])
def handle_video(message):
    file_id = message.video.file_id
    link = generate_link()
    video_links\\[link\\] = file_id
    bot.reply_to(message, f\"فیلم ذخیره شد ✅\\\\nلینک اختصاصی برای کاربران: /{link}\")

\\# لینک اختصاصی برای کاربران
@bot.message_handler(func=lambda m: m.text and m.text.startswith('/'))
def handle_link(message):
    link = message.text\\[1:\\]
    if link not in video_links:
        bot.reply_to(message, \"❌ لینک نامعتبر است.\")
        return

    user_id = message.from_user.id
    not_joined = check_membership(user_id)
    user_status\\[user_id\\] = not_joined

    if not_joined:
        markup = InlineKeyboardMarkup()
        for ch in not_joined:
            markup.add(InlineKeyboardButton(f\"عضو شدن در {ch}\", url=f\"https://t.me/{ch\\[1:\\]}\"))
        bot.reply_to(message, \"⚠️ ابتدا باید در کانال‌های زیر عضو شوید:\", reply_markup=markup)
    else:
        file_id = video_links\\[link\\]
        bot.send_video(message.chat.id, file_id)
        bot.reply_to(message, \"🎬 این فیلم برای شماست!\")

\\# دستور start
@bot.message_handler(commands=\\['start'\\])
def start(message):
    bot.reply_to(message, \"سلام! برای دریافت فیلم‌ها لینک اختصاصی دریافت کنید و ابتدا در کانال‌ها عضو شوید (اگر کانالی موجود باشد).\")

bot.infinity_polling()