from django.db import models

from .Product import Product


class WarehouseProducts(models.Model):
    product = models.OneToOneField(Product, on_delete=models.DO_NOTHING, verbose_name='Товар')
    count_products = models.PositiveSmallIntegerField(verbose_name='Количество товаров')

    class Meta:
        verbose_name_plural = 'Склад товаров'
        verbose_name = 'Ячейка для хранения одной позиции товара'
        ordering = ['product']

    def __str__(self):
        return self.product.title + ' с количеством ' + str(self.count_products)

