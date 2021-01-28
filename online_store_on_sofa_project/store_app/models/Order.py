from django.core import validators
from django.db import models

from .Recipient import Recipient


class Order(models.Model):
    """Модель оформленного заказа"""
    num_order = models.CharField(max_length=20, verbose_name='Номер заказа', blank=True, null=True, unique=True)
    created_at = models.DateTimeField(auto_now=True, verbose_name='Дата и время создания зказа', db_index=True)

    recipient = models.ForeignKey(Recipient, on_delete=models.CASCADE, verbose_name='Получатель')
    buyer_email = models.EmailField(verbose_name='Электронная почта покупателя')

    total_sum = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True,
                                    verbose_name='Итоговая цена заказа',
                                    validators=[validators.MinValueValidator(1), validators.MaxValueValidator(1000000)])
    payment_method = models.CharField(max_length=30, verbose_name='Способ оплаты')
    method_receive_order = models.CharField(max_length=30, verbose_name='Способ получения заказа', default='Самовывоз')

    date_order = models.DateField(db_index=True, verbose_name='Дата получения заказа', blank=True, null=True)

    def __str__(self):
        return f'{str(self.pk).zfill(6)}'

    class Meta:
        verbose_name_plural = 'Заказы'
        verbose_name = 'Заказ'
        ordering = ['date_order', 'num_order', 'buyer_email']