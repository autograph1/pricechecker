from .views import ProductLestCreateView, product_detail
from django.urls import path

urlpatterns = [
    path('products/', ProductLestCreateView.as_view()),
    path('products/<int:id>/', product_detail),
]
