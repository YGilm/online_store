from django.db import models

NULLABLE = {'null': True, 'blank': True}


class Category(models.Model):
    category_name = models.CharField(max_length=50, verbose_name='наименование')
    description = models.CharField(max_length=100, verbose_name='описание')

    def __str__(self):
        return self.category_name

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'
        ordering = ('category_name',)


class Product(models.Model):
    product_name = models.CharField(max_length=50, verbose_name='наименование')
    description = models.CharField(max_length=100, verbose_name='описание')
    product_image = models.ImageField(upload_to='product_image/', verbose_name='изображение', **NULLABLE)
    category = models.ForeignKey(Category, verbose_name='категория', on_delete=models.PROTECT)
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='цена за покупку')
    creation_date = models.DateField(auto_now_add=True, verbose_name='дата создания')
    last_modified_date = models.DateField(auto_now=True, verbose_name='дата последнего изменения')

    def __str__(self):
        return f'{self.product_name}, {self.purchase_price}, {self.description}'

    class Meta:
        verbose_name = 'продукт'
        verbose_name_plural = 'продукты'
        ordering = ('product_name',)
