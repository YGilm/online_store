from django.urls import path
from django.conf import settings

from catalog.apps import CatalogConfig
from catalog.views import home, contacts, product
from django.conf.urls.static import static
from catalog import views

app_name = CatalogConfig.name

urlpatterns = [
    path('', home, name='home'),
    path('contacts/', contacts, name='contacts'),
    path('product/', product, name='product'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
