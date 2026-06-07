import telebot

from users.models import User
from django.conf import settings


bot = telebot.TeleBot(settings.BOT_TOKEN)


@bot.message_handler(commands=['start'])
def start(message):

    user, created = User.objects.get_or_create(
        telegram_id=message.from_user.id,
        defaults={
            "username": f"tg_{message.from_user.id}"
        }
    )

    bot.send_message(
        message.chat.id,
        "Привет, я бот для отслеживания цен"
    )