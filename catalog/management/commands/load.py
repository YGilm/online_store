from django.core.management.base import BaseCommand
from django.core.management import call_command
from catalog.models import Category, Product


class Command(BaseCommand):
    """Удаляет старые данные и загружает новые из фикстур."""

    def handle(self, *args, **kwargs):
        # Удаление старых данных
        Product.objects.all().delete()
        Category.objects.all().delete()

        call_command('loaddata', 'store_data.json')

