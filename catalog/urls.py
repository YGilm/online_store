from django.urls import path
from django.conf import settings
from catalog.views import home, contacts, product
from django.conf.urls.static import static

urlpatterns = [
    path('', home),
    path('contacts/', contacts),
    path('product/', product)
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
