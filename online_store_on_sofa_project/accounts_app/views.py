import random
import string

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import render, redirect

from django.template.loader import render_to_string
from django.views import View
from .forms import RegisterForm, ActivationAccountForm, LoginForm
from .models import RegistrationConfirmationByEmail


def attribute_matching(attribute1, attribute2):
    """function of checking the correctness of the data entered by the user during registration"""
    if attribute1 == attribute2:
        return True
    else:
        return False


class LoginView(View):
    """
    Пользователь логинится на сайте, чтобы совершать дальнейшие покупки, если у него есть аккаунт,
    и пользователь подтвердил его с помощью электронной почты
    """

    def get(self, request):
        login_form = LoginForm()
        return render(request, 'login.html', {'form': login_form})

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            human = True
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            activation_state = RegistrationConfirmationByEmail.objects.get(username=username)
            user = authenticate(username=username, password=password)
            if user is not None and activation_state.is_confirmed:
                login(request, user)
                print('Welcome')
                return redirect('home')
            else:
                print('Try to login again')
                return self.get(request)


class LogoutView(View):
    """
    User logout
    """

    def get(self, request):
        logout(request)
        return redirect('home')


class SignUpView(View):
    """
    New User Registration
    """

    def get(self, request):
        form = RegisterForm()
        return render(request, 'signup.html', {'form': form})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            username = register_form.cleaned_data['username']
            email = register_form.cleaned_data['email']
            password = register_form.cleaned_data['password']
            password1 = register_form.cleaned_data['repeat_password']
            first_name = register_form.cleaned_data['first_name']
            last_name = register_form.cleaned_data['last_name']

            if attribute_matching(password, password1):
                user = User.objects.create_user(username=username,
                                                email=email,
                                                password=password,
                                                first_name=first_name,
                                                last_name=last_name)
                user.save()

                secret_code = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits)
                                      for _ in range(30))
                self.save_registration_attempt(email=email, code=secret_code, username=username)

                data = {'email': email, 'first_name': first_name, 'last_name': last_name, 'code': secret_code}
                self.send_letter_confirm_registration(data)

                return redirect('activate_account')
                # return render(request, 'activate_account.html', personal_data)
            else:

                return self.get(request)

    def save_registration_attempt(self, email, code, username):
        registration_attempt = RegistrationConfirmationByEmail()
        registration_attempt.email = email
        registration_attempt.activation_code = code
        registration_attempt.username = username
        registration_attempt.save()

    def send_letter_confirm_registration(self, data):
        html_body = render_to_string('confirmation_registration_email.html', data)
        msg = EmailMultiAlternatives(subject='Регистрация на сайте интернет-магазина TOP SHOP.', to=[data['email'], ])
        msg.attach_alternative(html_body, 'text/html')
        msg.send()


class ActivateAccountView(View):
    def __init__(self):
        self.attempts = 3

    def get(self, request):
        account_activation_form = ActivationAccountForm()
        return render(request, 'activate_account.html', {'form': account_activation_form})

    def post(self, request):
        account_activation_form = ActivationAccountForm(request.POST)
        if account_activation_form.is_valid():
            email = account_activation_form.cleaned_data['email']
            code = account_activation_form.cleaned_data['activation_code']

            user_activation = RegistrationConfirmationByEmail.objects.get(email=email)
            print(user_activation.activation_code == code)
            if user_activation is not None and attribute_matching(user_activation.activation_code, code):
                user_activation.is_confirmed = True
                user_activation.save()
                return redirect('login')

            else:
                self.attempts -= 1

                if self.attempts <= 0:
                    return redirect('home')
        return redirect('activate_account')
