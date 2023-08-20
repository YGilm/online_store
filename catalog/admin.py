from django.contrib import admin
from catalog.models import Category, Product


@admin.register(Category)
class Category(admin.ModelAdmin):
    list_display = ('id', 'category_name')


@admin.register(Product)
class Product(admin.ModelAdmin):
    list_display = ('id', 'category')
    list_filter = ('category',)
    search_fields = ('product_name', 'description',)
