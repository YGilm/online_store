from django.core.cache import cache
from config import settings
from .models import Category


def get_cached_categories():
    """
    Получает список всех категорий с использованием низкоуровневого кеширования.
    """
    if settings.CACHE_ENABLED:
        key = 'all_categories'
        categories = cache.get(key)

        if categories is None:
            categories = list(Category.objects.all())
            cache.set(key, categories, 3600)
        return categories

    else:
        return list(Category.objects.all())

