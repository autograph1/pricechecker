from .models import Product
from .serializers import ProductSerializer
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

class ProductListCreateView(ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer