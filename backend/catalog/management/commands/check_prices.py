from django.core.management import BaseCommand
from catalog.models import Product
from catalog.parsers import parse_ozon
class Command(BaseCommand):
    def handle(self, *args, **options):
        products = Product.objects.all()
        for product in products:
            data = parse_ozon(product.url)
            print(data)