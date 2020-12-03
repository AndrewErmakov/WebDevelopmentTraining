from django.contrib.auth.models import User
from django.core import validators
from django.db import models


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

    class Meta:
        verbose_name_plural = 'Товары'
        verbose_name = 'Товар'
        ordering = ['-sale_start_time']

    def __str__(self):
        return self.title


class ImageProduct(models.Model):
    """Модель изображения товара"""
    image = models.ImageField(null=True, blank=True, verbose_name='Изображения товара',
                              upload_to="images/store_app/products/",
                              validators=[validators.validate_image_file_extension])
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар')

    class Meta:
        verbose_name_plural = 'Изображения товаров'
        verbose_name = 'Изображение товара'
        ordering = ['product']

    def __str__(self):
        return self.product.title


class Comment(models.Model):
    """Модель комментария к товару"""
    text_comment = models.TextField(blank=True, null=True, verbose_name='Комментарий')
    rating = models.PositiveSmallIntegerField(validators=[validators.MaxValueValidator(5)], verbose_name='Оценка')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар')
    author_comment = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    data_comment = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Дата комментирования')

    class Meta:
        verbose_name_plural = 'Комментарии'
        verbose_name = 'Комментарий'
        ordering = ['product']

    def __str__(self):
        return self.product.title


class Rubric(models.Model):
    name = models.CharField(max_length=20, db_index=True, verbose_name='Название рубрики',
                            validators=[validators.MinLengthValidator(3)])

    class Meta:
        verbose_name_plural = 'Рубрики'
        verbose_name = 'Рубрика'
        ordering = ['name']

    def __str__(self):
        return self.name


class WarehouseProducts(models.Model):
    product = models.OneToOneField(Product, on_delete=models.DO_NOTHING, verbose_name='Товар')
    count_products = models.PositiveSmallIntegerField(verbose_name='Количество товаров')

    class Meta:
        verbose_name_plural = 'Склад товаров'
        verbose_name = 'Ячейка для хранения одной позиции товара'
        ordering = ['product']

    def __str__(self):
        return self.product.title + ' с количеством ' + self.count_products


class BasketUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Никнейм покупателя')
    products = models.ManyToManyField(Product, verbose_name='Товары в корзине')

    class Meta:
        verbose_name_plural = 'Корзина пользователя с товарами'
        verbose_name = 'Товар в корзине'
        ordering = ['user']

    def __str__(self):
        return self.user.username
