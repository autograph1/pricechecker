from django.core.management import BaseCommand
from catalog.models import Product

class Command(BaseCommand):
    def handle(self, *args, **options):
        products = Product.objects.all()
        print(products.count())
