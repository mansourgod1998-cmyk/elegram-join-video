import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import random
import string

TOKEN = \"توکن\\_ربات\\_تو\\_اینجا\"
CHANNELS = \\[\"@Channel1\", \"@Channel2\", \"@Channel3\"\\]

bot = telebot.TeleBot(TOKEN)

\\# دیتابیس ساده در مموری (اگر رستارت بشه، داده‌ها پاک می‌شوند)
video_links = {}  # format: { \"link8حرف\": \"file_id\" }
user_status = {}

def generate_link():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=8))

def check_membership(user_id):
    not_joined = \\[\\]
    for ch in CHANNELS:
        try:
            member = bot.get_chat_member(ch, user_id)
            if member.status in \\[\"left\", \"kicked\"\\]:
                not_joined.append(ch)
        except Exception:
            not_joined.append(ch)
    return not_joined

@bot.message_handler(content_types=\\['video'\\])
def handle_video(message):
    # وقتی تو فیلم می‌فرستی
    file_id = message.video.file_id
    link = generate_link()
    video_links\\[link\\] = file_id
    bot.reply_to(message, f\"فیلم ذخیره شد ✅\\\\nلینک اختصاصی برای کاربران: /{link}\")

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

@bot.message_handler(commands=\\['start'\\])
def cmd_start(message):
    bot.reply_to(message, \"سلام! یک لینک فیلم از من بگیر، اول باید جوین سه کانال بشی تا بتونی فیلم رو دانلود کنی.\")

bot.infinity_polling()