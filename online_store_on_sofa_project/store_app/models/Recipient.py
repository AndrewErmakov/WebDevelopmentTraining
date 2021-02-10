from django.db import models


class Recipient(models.Model):
    """Модель получателя заказа"""
    name_recipient = models.CharField(max_length=50, verbose_name='Имя получателя заказа', blank=True, null=True)
    surname_recipient = models.CharField(max_length=50, verbose_name='Фамилия получателя заказа', blank=True, null=True)
    phone_recipient = models.CharField(max_length=15, verbose_name='Номер телефона получателя заказа', blank=True,
                                       null=True)

    class Meta:
        verbose_name_plural = 'Получатели заказа'
        verbose_name = 'Получатель заказа'
        ordering = ['name_recipient', 'surname_recipient']

    def __str__(self):
        return f'{self.name_recipient} {self.surname_recipient}'