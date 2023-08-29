from django.urls import path

from catalog.views import home, contacts, product

urlpatterns = [
    path('', home),
    path('contacts/', contacts),
    path('product/', product)
]

