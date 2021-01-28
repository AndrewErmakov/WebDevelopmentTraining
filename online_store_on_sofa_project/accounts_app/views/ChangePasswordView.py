from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect
from django.views import View

from accounts_app.forms import ChangePasswordForm
from accounts_app.views import validation_recaptcha_v2


class ChangePasswordView(View, LoginRequiredMixin):
    """Класс страницы смены пароля авторизованным пользователем,
    если он не авторизован - попадает на страницу входа в аккаунт"""

    raise_exception = True

    def get(self, request):
        try:
            change_password_form = ChangePasswordForm()
            return render(request, 'change_password.html', {'form': change_password_form,
                                                            'title': 'Смена пароля',
                                                            'GOOGLE_RECAPTCHA_SITE_KEY': settings.GOOGLE_RECAPTCHA_SITE_KEY})

        except PermissionDenied:
            return redirect('login')

    def post(self, request):
        change_password_form = ChangePasswordForm(request.POST)
        if change_password_form.is_valid():
            if request.user.check_password(change_password_form.cleaned_data['old_password']) and \
                    validation_recaptcha_v2(request):
                request.user.set_password(change_password_form.cleaned_data['new_password'])
                request.user.save()
                return redirect('home')
            else:
                return render(request, 'change_password.html', {'form': ChangePasswordForm(request.GET),
                                                                'title': 'Смена пароля. Попытайтесь еще раз',
                                                                'GOOGLE_RECAPTCHA_SITE_KEY': settings.GOOGLE_RECAPTCHA_SITE_KEY})
        else:
            self.get(request)