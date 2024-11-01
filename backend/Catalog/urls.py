from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (CategoryViewSet, ProductTypeViewSet, BrandViewSet, CurrencyViewSet,
                    ParameterViewSet, ProductParameterViewSet, ProductImageViewSet,
                    TagViewSet, ProductTagViewSet, ReportViewSet, ProductViewSet)

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'product-types', ProductTypeViewSet)
router.register(r'brands', BrandViewSet)
router.register(r'currencies', CurrencyViewSet)
router.register(r'parameters', ParameterViewSet)
router.register(r'product-parameters', ProductParameterViewSet)
router.register(r'product-images', ProductImageViewSet)
router.register(r'tags', TagViewSet)
router.register(r'product-tags', ProductTagViewSet)
router.register(r'reports', ReportViewSet)
router.register(r'products', ProductViewSet)

urlpatterns = [
    path('', include(router.urls)),
]