from django.contrib.auth.models import User
from django.db import models

from .Product import Product


class CartUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Никнейм покупателя')
    products = models.ManyToManyField(Product, verbose_name='Товары в корзине')

    class Meta:
        verbose_name_plural = 'Корзина пользователя с товарами'
        verbose_name = 'Товар в корзине'
        ordering = ['user']

    def __str__(self):
        return 'Корзина пользователя с товарами ' + self.user.username