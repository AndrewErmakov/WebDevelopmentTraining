from accounts_app.forms import ActivationAccountForm
from accounts_app.models import RegistrationConfirmationByEmail
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views import View


class ActivateAccountView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.attempts = 3

    def get(self, request):
        if request.user.is_anonymous:
            account_activation_form = ActivationAccountForm()
            return render(request, 'activate_account.html', {'form': account_activation_form})
        else:
            return redirect('home')

    def post(self, request):
        account_activation_form = ActivationAccountForm(request.POST)
        if account_activation_form.is_valid():
            email = account_activation_form.cleaned_data['email']
            code = account_activation_form.cleaned_data['activation_code']

            user_activation = RegistrationConfirmationByEmail.objects.get(
                user=User.objects.get(email=email))

            if user_activation is not None and user_activation.activation_code == code:
                user_activation.is_confirmed = True
                user_activation.save()
                return redirect('login')

            else:
                self.attempts -= 1

                if self.attempts <= 0:
                    return redirect('home')

        return redirect('activate_account')
