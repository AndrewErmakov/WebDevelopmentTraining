from django.core import validators
from django.db import models

from .Product import Product


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
