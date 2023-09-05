from django.urls import path
from django.conf import settings

from catalog.apps import CatalogConfig
from catalog.views import *
from django.conf.urls.static import static

app_name = CatalogConfig.name

urlpatterns = [
    path('', HomeListView.as_view(), name='home'),
    path('contacts/', contacts, name='contacts'),
    path('product/', ProductListView.as_view(), name='product_list'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('blogs/', BlogPostListView.as_view(), name='blogs'),
    path('blogs/<int:pk>/', BlogPostDetailView.as_view(), name='blogpost_detail'),
    path('create/', BlogPostCreateView.as_view(), name='blogpost_form'),
    path('blogs/edit/<int:pk>/', BlogPostUpdateView.as_view(), name='blogpost_update'),
    path('blogs/delete/<int:pk>/', BlogPostDeleteView.as_view(), name='blogpost_delete')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
