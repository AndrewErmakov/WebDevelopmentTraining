from django.core import validators
from django.db import models


class RegistrationConfirmationByEmail(models.Model):
    email = models.EmailField()
    is_confirmed = models.BooleanField(default=False)
    activation_code = models.CharField(max_length=30, validators=[validators.MinLengthValidator(30)],
                                       default='123456789009876543211234567890')
    username = models.CharField(max_length=30, default='new_user')

    class Meta:
        verbose_name_plural = 'Подтверждения регистрации'

    def __str__(self):
        return self.email
