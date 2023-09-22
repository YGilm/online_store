from django.db import models
from autoslug import AutoSlugField

NULLABLE = {'null': True, 'blank': True}


class Category(models.Model):
    """
    Модель для хранения информации о категориях продуктов.
    """
    category_name = models.CharField(max_length=50, verbose_name='наименование')
    description = models.CharField(max_length=100, verbose_name='описание')

    def __str__(self):
        return self.category_name

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'
        ordering = ('category_name',)


class Product(models.Model):
    """
    Модель для хранения информации о продуктах.
    Содержит информацию о наименовании, описании, цене и категории продукта.
    """
    product_name = models.CharField(max_length=50, verbose_name='наименование')
    description = models.CharField(max_length=100, verbose_name='описание')
    product_image = models.ImageField(upload_to='products/', verbose_name='изображение', **NULLABLE)
    category = models.ForeignKey(Category, verbose_name='категория', on_delete=models.PROTECT)
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='цена за покупку')
    creation_date = models.DateField(auto_now_add=True, verbose_name='дата создания')
    last_modified_date = models.DateField(auto_now=True, verbose_name='дата последнего изменения')

    def __str__(self):
        return f'{self.product_name}, {self.description} {self.purchase_price}'

    class Meta:
        verbose_name = 'продукт'
        verbose_name_plural = 'продукты'
        ordering = ('product_name',)


class BlogPost(models.Model):
    """
    Модель для хранения блогов.
    Содержит заголовок, содержание, изображение и информацию о публикации.
    """
    title = models.CharField(max_length=150, verbose_name='заголовок')
    slug = AutoSlugField(populate_from='title', unique=True, verbose_name='slug')
    content = models.TextField(verbose_name='содержание')
    image = models.ImageField(upload_to='blog/', verbose_name='изображение', **NULLABLE)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='дата создания')
    is_published = models.BooleanField(default=True, verbose_name='опубликован')
    views_count = models.IntegerField(default=0, verbose_name='количество просмотров')

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = 'блог'
        verbose_name_plural = 'блоги'
        ordering = ('created_at',)


class Version(models.Model):
    """
    Модель для хранения информации о версии продукта.
    Содержит информацию о номере, названии, и признаке текущей версии.
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='наименование продукта')
    version_number = models.CharField(max_length=20, verbose_name='номер версии')
    version_name = models.CharField(max_length=150, verbose_name='название версии')
    is_current = models.BooleanField(default=False, verbose_name='активная', **NULLABLE)

    def __str__(self):
        return f'{self.product}, {self.version_number} {self.version_name}'

    class Meta:
        verbose_name = 'версия'
        verbose_name_plural = 'версии'
