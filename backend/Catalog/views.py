from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from .models import Category, ProductType, Brand, Currency, Parameter, ProductParameter, ProductImage, Tag, ProductTag, Report, Product
from .serializers import (CategorySerializer, ProductTypeSerializer, BrandSerializer, CurrencySerializer,
                          ParameterSerializer, ProductParameterSerializer, ProductImageSerializer,
                          TagSerializer, ProductTagSerializer, ReportSerializer, ProductSerializer)

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class ProductTypeViewSet(viewsets.ModelViewSet):
    queryset = ProductType.objects.all()
    serializer_class = ProductTypeSerializer

class BrandViewSet(viewsets.ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer

class CurrencyViewSet(viewsets.ModelViewSet):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer

class ParameterViewSet(viewsets.ModelViewSet):
    queryset = Parameter.objects.all()
    serializer_class = ParameterSerializer

class ProductParameterViewSet(viewsets.ModelViewSet):
    queryset = ProductParameter.objects.all()
    serializer_class = ProductParameterSerializer

class ProductImageViewSet(viewsets.ModelViewSet):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer

class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

class ProductTagViewSet(viewsets.ModelViewSet):
    queryset = ProductTag.objects.all()
    serializer_class = ProductTagSerializer

class ReportViewSet(viewsets.ModelViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer


class ProductPagination(PageNumberPagination):
    page_size = 30
    page_size_query_param = 'limit'
    max_page_size = 100

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = ProductPagination

    def list(self, request, *args, **kwargs):
        category_id = request.query_params.get('category')
        parameters = request.data.get('parameters', [])
        
        limit = request.query_params.get('limit', self.pagination_class.page_size)
        try:
            limit = min(int(limit), self.pagination_class.max_page_size)
        except (ValueError, TypeError):
            limit = self.pagination_class.page_size

        queryset = self.queryset

        if category_id:
            queryset = queryset.filter(category_id=category_id)

        if parameters:
            for param in parameters:
                param_name = param.get('name')
                param_value = param.get('value')
                if param_name and param_value:
                    queryset = queryset.filter(parameters__parameter__name=param_name, parameters__value=param_value)

        self.pagination_class.page_size = limit
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)