# Generated by Django 4.2.4 on 2023-08-20 16:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0002_alter_product_purchase_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='creation_date',
            field=models.DateField(auto_now_add=True, verbose_name='дата создания'),
        ),
        migrations.AlterField(
            model_name='product',
            name='last_modified_date',
            field=models.DateField(auto_now=True, verbose_name='дата последнего изменения'),
        ),
    ]
