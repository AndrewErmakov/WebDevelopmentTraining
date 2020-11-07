from django.contrib import admin
from .models import RegistrationConfirmationByEmail

admin.site.register(RegistrationConfirmationByEmail)


class RegistrationConfirmationByEmailAdminL:
    list_display = ('email', 'is_confirmed', 'activation_code')
    list_display_links = 'email'
    search_fields = ('email',)
