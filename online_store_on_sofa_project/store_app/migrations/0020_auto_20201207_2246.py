# Generated by Django 3.1.3 on 2020-12-07 17:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store_app', '0019_auto_20201207_2226'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductInCart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count_product_in_cart', models.PositiveIntegerField(default=1, verbose_name='Количество данного товара')),
                ('cart_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='store_app.cartuser', verbose_name='Никнейм пользователя - владельца корзины')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store_app.product', verbose_name='Название товара')),
            ],
            options={
                'verbose_name_plural': 'Количество определенного товара в корзине',
                'ordering': ['cart_user'],
            },
        ),
        migrations.DeleteModel(
            name='CountProductInCart',
        ),
    ]
