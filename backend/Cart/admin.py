from django.contrib import admin
from .models import Cart, CartItem

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 1  # Количество пустых форм для добавления новых элементов

class CartAdmin(admin.ModelAdmin):
    inlines = [CartItemInline]
    list_display = ('user', 'created_at')  # Поля для отображения в списке
    search_fields = ('user__username',)  # Поиск по имени пользователя

admin.site.register(Cart, CartAdmin)