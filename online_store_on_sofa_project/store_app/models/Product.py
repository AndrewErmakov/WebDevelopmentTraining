from django.core import validators
from django.db import models
from django.db.models import Avg


class Product(models.Model):
    """Модель описания товара"""
    title = models.CharField(max_length=50, verbose_name='Название товара',
                             validators=[validators.MinLengthValidator(5)])
    description = models.TextField(blank=True, null=True, verbose_name='Описание',
                                   validators=[validators.MinLengthValidator(15)])
    price = models.DecimalField(max_digits=9, decimal_places=2,
                                blank=True, null=True, verbose_name='Цена',
                                validators=[
                                    validators.MinValueValidator(1),
                                    validators.MaxValueValidator(1000000)])
    brand = models.CharField(max_length=50, verbose_name='Бренд',
                             validators=[validators.MinLengthValidator(2)])
    sale_start_time = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Дата начала продажи')
    rubric = models.ForeignKey('Rubric', on_delete=models.PROTECT, null=True, verbose_name='Рубрика')
    avg_rating = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True,
                                     verbose_name='Рейтинг товара', default=-1,
                                     validators=[
                                         validators.MinValueValidator(1),
                                         validators.MaxValueValidator(5)]
                                     )


    class Meta:
        verbose_name_plural = 'Товары'
        verbose_name = 'Товар'
        ordering = ['-sale_start_time']

    def __str__(self):
        return self.title

