from django.shortcuts import render
from catalog.models import *


def home(request):
    unique_categories = Product.objects.order_by('category').values_list('category', flat=True).distinct()
    product_list = [Product.objects.filter(category=cat).first() for cat in unique_categories]
    context = {
        'object_list': product_list[:3]
    }
    return render(request, 'catalog/home.html', context)


def product(request):
    product_list = Product.objects.all()
    context = {
        'object_list': product_list
    }
    return render(request, 'catalog/product.html', context)


def contacts(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        print(f'У вас новый запрос на обратную связь: {name} {phone}: {message}')
    return render(request, 'catalog/contacts.html')
