from django.core import validators
from django.db import models


class FeedBackWithClient(models.Model):
    """Модель обращения клиентов с просьбой об обратной связи"""
    name_client = models.CharField(max_length=50, verbose_name='Имя клиента',
                                   validators=[validators.MinLengthValidator(5)])
    phone_client = models.CharField(max_length=15, verbose_name='Номер телефона для обратной связи')
    email_client = models.EmailField(verbose_name='Электронная почта для обратной связи',
                                     validators=[validators.MinLengthValidator(5)])

    question_client = models.TextField(verbose_name='Вопрос клиента', validators=[validators.MinLengthValidator(15)],
                                       null=True)
    given_feedback = models.BooleanField(verbose_name='Дана ли обратная связь?', default=False)

    def __str__(self):
        return f'Заявка на обратную связь №{str(self.pk).zfill(6)}'

    class Meta:
        verbose_name_plural = 'Заявки на обратную связь'
        verbose_name = 'Заявка на обратную связь'
        ordering = ['name_client', 'phone_client', 'email_client', 'given_feedback']