from django.contrib import admin
from .models import RegistrationConfirmationByEmail

admin.site.register(RegistrationConfirmationByEmail)


class RegistrationConfirmationByEmailAdmin:
    list_display = ('user', 'is_confirmed', 'activation_code')
    list_display_links = ['user', 'activation_code']
    search_fields = ('user', 'activation_code',)
