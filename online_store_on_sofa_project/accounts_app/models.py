from django.contrib.auth.models import User
from django.core import validators
from django.db import models


class RegistrationConfirmationByEmail(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    is_confirmed = models.BooleanField(default=False)
    activation_code = models.CharField(max_length=30, validators=[validators.MinLengthValidator(30)],
                                       default='123456789009876543211234567890')

    class Meta:
        verbose_name_plural = 'Подтверждения регистрации'

    def __str__(self):
        return self.user.email

