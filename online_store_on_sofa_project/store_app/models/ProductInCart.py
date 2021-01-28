from django.db import models

from .Product import Product
from .CartUser import CartUser


class ProductInCart(models.Model):
    """Модель одной позиции товара в корзине"""
    cart_user = models.ForeignKey(CartUser, on_delete=models.CASCADE,
                                  verbose_name='Никнейм пользователя - владельца корзины', blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Название товара')
    count_product_in_cart = models.PositiveIntegerField(default=1, verbose_name='Количество данного товара')

    def __str__(self):
        return f'В корзине {self.cart_user.user.username} лежит товар {self.product.title} в количестве ' \
               f'{self.count_product_in_cart}'

    class Meta:
        verbose_name_plural = 'Количество определенного товара в корзине'
        ordering = ['cart_user']
