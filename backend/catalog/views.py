from .models import Product
from .serializers import ProductSerializer
from rest_framework.viewsets import ModelViewSet

class ProductListSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
