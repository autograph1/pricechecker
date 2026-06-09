import telebot

from django.conf import settings

from users.models import User
from catalog.models import Product
from catalog.parsers_citilink import parse_citilink


waiting_for_link = []

bot = telebot.TeleBot(settings.BOT_TOKEN)

@bot.message_handler(commands=['price'])
def set_price(message):

    try:

        parts = message.text.split()

        product_id = int(parts[1])
        needed_price = int(parts[2])

        user = User.objects.get(
            telegram_id=message.from_user.id
        )

        product = Product.objects.get(
            id=product_id,
            owner=user
        )

        product.needed_price = needed_price
        product.save()

        bot.send_message(
            message.chat.id,
            f"""
🎯 Целевая цена установлена

📦 {product.title}

💰 Желаемая цена: {needed_price} ₽
            """
        )

    except IndexError:

        bot.send_message(
            message.chat.id,
            "Использование:\n/price ID ЦЕНА"
        )

    except ValueError:

        bot.send_message(
            message.chat.id,
            "Цена и ID должны быть числами"
        )

    except Product.DoesNotExist:

        bot.send_message(
            message.chat.id,
            "Товар не найден"
        )

@bot.message_handler(commands=['delete'])
def delete_product(message):

    try:
        product_id = int(message.text.split()[1])

        user = User.objects.get(
            telegram_id=message.from_user.id
        )

        product = Product.objects.get(
            id=product_id,
            owner=user
        )

        title = product.title

        product.delete()

        bot.send_message(
            message.chat.id,
            f"🗑 Товар удалён\n\n{title}"
        )

    except IndexError:

        bot.send_message(
            message.chat.id,
            "Использование:\n/delete ID"
        )

    except Product.DoesNotExist:

        bot.send_message(
            message.chat.id,
            "Товар не найден"
        )


@bot.message_handler(commands=['start'])
def start(message):

    User.objects.get_or_create(
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


@bot.message_handler(commands=['list'])
def list_products(message):

    print("LIST COMMAND")

    user = User.objects.get(
        telegram_id=message.from_user.id
    )

    products = Product.objects.filter(
        owner=user
    )

    if not products.exists():

        bot.send_message(
            message.chat.id,
            "У вас пока нет товаров"
        )

        return

    text = "📦 Ваши товары:\n\n"

    for product in products:

        text += (
            f"{product.id}. {product.title}\n"
            f"💰 {product.current_price} ₽\n\n"
        )

    bot.send_message(
        message.chat.id,
        text
    )


@bot.message_handler(func=lambda message: True)
def handle_message(message):

    if message.text.startswith("/"):
        return

    if message.from_user.id in waiting_for_link:

        try:

            user = User.objects.get(
                telegram_id=message.from_user.id
            )

            product = Product.objects.create(
                owner=user,
                url=message.text,
                needed_price=0
            )

            data = parse_citilink(
                message.text
            )

            product.title = data["title"]
            product.current_price = data["price"]
            product.save()

            bot.send_message(
                message.chat.id,
                f"""
✅ Товар добавлен

📦 {product.title}

💰 Текущая цена: {product.current_price} ₽
                """
            )

        except Exception as e:

            bot.send_message(
                message.chat.id,
                f"Ошибка: {e}"
            )

        finally:

            if message.from_user.id in waiting_for_link:
                waiting_for_link.remove(
                    message.from_user.id
                )


