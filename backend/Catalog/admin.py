from django.contrib import admin
from .models import (
    Category,
    Brand,
    Product,
    ProductType,
    Currency,
    Parameter,
    ProductParameter,
    ProductImage,
    Tag,
    ProductTag,
    Report
)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at', 'updated_at')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}  # Если slug нужен

class BrandAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at', 'updated_at')
    search_fields = ('name',)

class ProductTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at', 'updated_at')
    search_fields = ('name',)

class CurrencyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'symbol', 'exchange_rate')
    search_fields = ('name',)

class ParameterAdmin(admin.ModelAdmin):
    list_display = ('id', 'category', 'name')
    search_fields = ('name',)

class ProductParameterAdmin(admin.ModelAdmin):
    list_display = ('id', 'parameter', 'value')
    search_fields = ('value',)

class ProductImageAdmin(admin.TabularInline):
    model = ProductImage
    extra = 1  # Количество дополнительных полей для добавления

class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'brand', 'price', 'created_at', 'updated_at')
    search_fields = ('name', 'reference_number')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductImageAdmin]
    list_filter = ('category', 'brand')

class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

class ProductTagAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'tag')

class ReportAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'date', 'sales_count', 'revenue')
    list_filter = ('date',)
    search_fields = ('product__name',)

# Регистрация моделей в админке
admin.site.register(Category, CategoryAdmin)
admin.site.register(Brand, BrandAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductType, ProductTypeAdmin)
admin.site.register(Currency, CurrencyAdmin)
admin.site.register(Parameter, ParameterAdmin)
admin.site.register(ProductParameter, ProductParameterAdmin)
admin.site.register(ProductImage)  # Отдельно, т.к. уже подключен через ProductAdmin
admin.site.register(Tag, TagAdmin)
admin.site.register(ProductTag, ProductTagAdmin)
admin.site.register(Report, ReportAdmin)