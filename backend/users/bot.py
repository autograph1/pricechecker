import telebot

from django.conf import settings

from users.models import User
from catalog.models import Product


waiting_for_link = []

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


@bot.message_handler(commands=['add'])
def add_product(message):

    if message.from_user.id not in waiting_for_link:
        waiting_for_link.append(message.from_user.id)

    bot.send_message(
        message.chat.id,
        "Пришли ссылку на товар"
    )


@bot.message_handler(func=lambda message: True)
def handle_message(message):

    if message.from_user.id in waiting_for_link:

        try:
            user = User.objects.get(
                telegram_id=message.from_user.id
            )

            Product.objects.create(
                owner=user,
                url=message.text,
                needed_price=0
            )

            bot.send_message(
                message.chat.id,
                "Товар добавлен"
            )

        except Exception as e:

            bot.send_message(
                message.chat.id,
                f"Ошибка: {e}"
            )

        finally:

            waiting_for_link.remove(message.from_user.id)