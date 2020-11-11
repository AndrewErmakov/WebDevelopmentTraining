from django.core import validators
from django.db import models


class Product(models.Model):
    title = models.CharField(max_length=50, verbose_name='Товар',
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
    image_product = models.ImageField(null=True, blank=True, verbose_name='Изображения товара', upload_to="images/",
                                      validators=[validators.validate_image_file_extension])

    class Meta:
        verbose_name_plural = 'Объявления'
        verbose_name = 'Объявление'
        ordering = ['-sale_start_time']


class Rubric(models.Model):
    name = models.CharField(max_length=20, db_index=True, verbose_name='Название рубрики',
                            validators=[validators.MinLengthValidator(3)])

    class Meta:
        verbose_name_plural = 'Рубрики'
        verbose_name = 'Рубрика'
        ordering = ['name']

    def __str__(self):
        return self.name
