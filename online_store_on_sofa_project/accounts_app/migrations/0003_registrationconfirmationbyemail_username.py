# Generated by Django 3.1.3 on 2020-11-07 18:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts_app', '0002_auto_20201107_2154'),
    ]

    operations = [
        migrations.AddField(
            model_name='registrationconfirmationbyemail',
            name='username',
            field=models.CharField(default='new_user', max_length=30),
        ),
    ]
