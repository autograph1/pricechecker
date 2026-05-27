from .views import ProductListCreateView, ProductDetailView
from django.urls import path

urlpatterns = [
    path('products/', ProductListCreateView.as_view()),
    path('products/<int:id>/', ProductDetailView.as_view()),
]
