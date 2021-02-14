from accounts_app.forms import ChangePasswordForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect
from django.views import View


class ChangePasswordView(View, LoginRequiredMixin):
    """Класс страницы смены пароля авторизованным пользователем,
    если он не авторизован - попадает на страницу входа в аккаунт"""

    raise_exception = True

    def get(self, request):
        try:
            change_password_form = ChangePasswordForm()
            return render(request, 'change_password.html', {'form': change_password_form,
                                                            'title': 'Смена пароля'})

        except PermissionDenied:
            return redirect('login')

    def post(self, request):
        change_password_form = ChangePasswordForm(request.POST)
        if change_password_form.is_valid():
            if request.user.check_password(change_password_form.cleaned_data['old_password']):
                request.user.set_password(change_password_form.cleaned_data['new_password'])
                request.user.save()
                return redirect('home')
            else:
                return render(request, 'change_password.html', {'form': ChangePasswordForm(request.GET),
                                                                'title': 'Смена пароля. Попытайтесь еще раз'})
        else:
            self.get(request)
