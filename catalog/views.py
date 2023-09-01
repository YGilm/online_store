from django.shortcuts import render, get_object_or_404
from catalog.models import *


def home(request):
    categories = Category.objects.all()
    top_products = []

    for category in categories:
        top_product = Product.objects.filter(category=category).order_by('-creation_date').first()
        if top_product:
            top_products.append(top_product)

    context = {
        'object_list': top_products[:3],  # Отправляем только первые три топовых продукта
        'title': 'home page'
    }
    return render(request, 'catalog/home.html', context)


def product(request):
    product_list = Product.objects.all()
    context = {
        'object_list': product_list,
        'title': 'catalog'
    }
    return render(request, 'catalog/product.html', context)


def contacts(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        print(f'У вас новый запрос на обратную связь: {name} {phone}: {message}')

    context = {
        'title': 'contacts'
        }
    return render(request, 'catalog/contacts.html', context)


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    context = {
        'object': product,
        'title': product.product_name
    }
    return render(request, 'catalog/product_detail.html', context)
