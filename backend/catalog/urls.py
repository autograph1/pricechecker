from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import ProductListSet

router = DefaultRouter()
router.register('products', ProductListSet)

urlpatterns = router.urls