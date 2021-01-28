from django.db import models

from .Product import Product
from .Order import Order


class ProductsInOrder(models.Model):
    """Модель товаров в заказе"""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='Заказ', null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Название товара')
    count_product_in_order = models.PositiveIntegerField(verbose_name='Количество данного товара')

    def __str__(self):
        return f'Заказ №{str(Order.num_order).zfill(6)}.'

    class Meta:
        verbose_name_plural = 'Товары в заказах'
        verbose_name = 'Товар в заказе'
        ordering = ['product', 'count_product_in_order']
