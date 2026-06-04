from django.core.management import BaseCommand
from catalog.models import Product
from catalog.parsers import parse_ozon
class Command(BaseCommand):
    def handle(self, *args, **options):
        products = Product.objects.all()
        for product in products:
            data = parse_ozon(product.url)
            product.current_price = data["price"]
            product.save()
            print("Проверяю")
            if product.current_price <= product.needed_price:
                print("Цена достигнута")
