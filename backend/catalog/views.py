from .models import Product
from .serializers import ProductSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .parsers import parse_ozon
class ProductListSet(ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        url = serializer.validated_data["url"]

        data = parse_ozon(url)

        serializer.save(
            owner=self.request.user,
            title=data["title"],
            current_price=data["price"],
        )

    def get_queryset(self):
        return Product.objects.filter(owner=self.request.user)