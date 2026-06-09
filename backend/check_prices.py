import os
import django
import telebot

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

from django.conf import settings
from catalog.models import Product
from catalog.parsers_citilink import parse_citilink


bot = telebot.TeleBot(settings.BOT_TOKEN)

products = Product.objects.all()

for product in products:

    try:

        data = parse_citilink(product.url)

        new_price = data["price"]

        if (
            product.needed_price > 0
            and new_price <= product.needed_price
        ):

            bot.send_message(
                product.owner.telegram_id,
                f"""
🎯 Цена достигнута

📦 {product.title}

💰 Текущая цена: {new_price} ₽

🎯 Желаемая цена: {product.needed_price} ₽

🗑 Товар автоматически удалён из отслеживания
                """
            )

            print(
                f"Цена достигнута: {product.title}"
            )

            product.delete()

            continue

        product.current_price = new_price
        product.save()

    except Exception as e:

        print(
            f"Ошибка для товара {product.id}: {e}"
        )