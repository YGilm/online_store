from django.urls import path
from django.conf import settings
from django.views.decorators.cache import cache_page

from catalog.apps import CatalogConfig
from catalog.views import *
from django.conf.urls.static import static

app_name = CatalogConfig.name

# Определение URL-шаблонов для приложения каталога
urlpatterns = [
    path('', HomeListView.as_view(), name='home'),
    path('contacts/', contacts, name='contacts'),
    path('product/', ProductListView.as_view(), name='product_list'),
    path('product/create/', never_cache(ProductCreateView.as_view()), name='product_form'),
    path('product/update/<int:pk>/', never_cache(ProductUpdateView.as_view()), name='product_update'),
    path('product/delete/<int:pk>/', ProductDeleteView.as_view(), name='product_delete'),
    path('product/<int:pk>/', cache_page(60)(ProductDetailView.as_view()), name='product_detail'),

    path('blogs/', BlogPostListView.as_view(), name='blogs'),
    path('blogs/<int:pk>/', BlogPostDetailView.as_view(), name='blogpost_detail'),
    path('blogs/create/', never_cache(BlogPostCreateView.as_view()), name='blogpost_form'),
    path('blogs/edit/<int:pk>/', never_cache(BlogPostUpdateView.as_view()), name='blogpost_update'),
    path('blogs/delete/<int:pk>/', BlogPostDeleteView.as_view(), name='blogpost_delete')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
