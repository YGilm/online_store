from django.contrib import admin
from catalog.models import Category, Product


@admin.register(Category)
class Category(admin.ModelAdmin):
    list_display = ('id', 'category_name', 'description',)


@admin.register(Product)
class Product(admin.ModelAdmin):
    list_display = ('id', 'product_name', 'description', 'category', 'purchase_price',)
    list_filter = ('category', 'purchase_price',)
    search_fields = ('product_name', 'description',)
