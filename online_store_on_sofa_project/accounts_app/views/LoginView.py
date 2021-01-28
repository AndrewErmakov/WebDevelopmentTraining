from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render
from django.views import View

from accounts_app.forms import LoginForm
from accounts_app.models import RegistrationConfirmationByEmail


class LoginView(View):
    """
    Пользователь логинится на сайте, чтобы совершать дальнейшие покупки, если у него есть аккаунт,
    и пользователь подтвердил его с помощью электронной почты
    """

    def get(self, request):
        if request.user.is_authenticated:
            redirect('home')
        else:
            login_form = LoginForm()
            return render(request, 'login.html', {'form': login_form})

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']

            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_superuser:
                    login(request, user)
                    return redirect('home')

                activation_state = RegistrationConfirmationByEmail.objects.get(user=user)
                if activation_state is not None:
                    if activation_state.is_confirmed:
                        login(request, user)
                        return redirect('home')
                    else:
                        return redirect('activate_account')
                else:
                    return redirect('signup')
            else:
                redirect('signup')

        else:
            return self.get(request)