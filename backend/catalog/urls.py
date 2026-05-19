from .views import product_list, product_detail
from django.urls import path

urlpatterns = [
    path('products/', product_list),
    path('products/<int:id>/', product_detail),
]
