from django.contrib.auth.models import User
from django.core import validators
from django.db import models
from django.utils import timezone


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

    count_reviews = models.PositiveIntegerField(verbose_name='Число отзывов на товар', default=0)

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
    date_comment = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Дата комментирования')

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
        return self.product.title + ' с количеством ' + str(self.count_products)


"""Модели, относящиеся к корзине"""


class CartUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Никнейм покупателя')
    products = models.ManyToManyField(Product, verbose_name='Товары в корзине')

    class Meta:
        verbose_name_plural = 'Корзина пользователя с товарами'
        verbose_name = 'Товар в корзине'
        ordering = ['user']

    def __str__(self):
        return 'Корзина пользователя с товарами ' + self.user.username


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


"""Модели, относящиеся к заказу"""


class Recipient(models.Model):
    """Модель получателя заказа"""
    name_recipient = models.CharField(max_length=50, verbose_name='Имя получателя заказа', blank=True, null=True)
    surname_recipient = models.CharField(max_length=50, verbose_name='Фамилия получателя заказа', blank=True, null=True)
    phone_recipient = models.CharField(max_length=14, verbose_name='Номер телефона получателя заказа', blank=True,
                                       null=True)

    class Meta:
        verbose_name_plural = 'Получатели заказа'
        verbose_name = 'Получатель заказа'
        ordering = ['name_recipient', 'surname_recipient']

    def __str__(self):
        return f'{self.name_recipient} {self.surname_recipient}'


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


class FeedBackWithClient(models.Model):
    """Модель обращения клиентов с просьбой об обратной связи"""
    name_client = models.CharField(max_length=50, verbose_name='Имя клиента',
                                   validators=[validators.MinLengthValidator(5)])
    phone_client = models.CharField(max_length=14, verbose_name='Номер телефона для обратной связи')
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
