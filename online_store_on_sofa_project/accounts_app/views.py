import json
import random
import string
import requests

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import render, redirect
from django.conf import settings
from django.template.loader import render_to_string
from django.views import View

from .forms import *
from .models import RegistrationConfirmationByEmail
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import PasswordResetForm
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse


# from g_recaptcha.validate_recaptcha import validate_captcha


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
        if request.user.is_anonymous:
            form = RegisterForm()
            return render(request, 'signup.html', {'form': form})
        else:
            return redirect('home')

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            username = register_form.cleaned_data['username']
            email = register_form.cleaned_data['email']
            password = register_form.cleaned_data['password']
            password1 = register_form.cleaned_data['repeat_password']
            first_name = register_form.cleaned_data['first_name']
            last_name = register_form.cleaned_data['last_name']

            if password == password1:
                user = User.objects.create_user(username=username,
                                                email=email,
                                                password=password,
                                                first_name=first_name,
                                                last_name=last_name)
                user.save()

                secret_code = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits)
                                      for _ in range(30))
                self.save_registration_attempt(user=user, code=secret_code)

                data = {'email': email, 'first_name': first_name, 'last_name': last_name, 'code': secret_code}
                self.send_letter_confirm_registration(data)

                return redirect('activate_account')
                # return render(request, 'activate_account.html', personal_data)
            else:

                return self.get(request)

    def save_registration_attempt(self, user, code):
        registration_attempt = RegistrationConfirmationByEmail()
        registration_attempt.user = user
        registration_attempt.activation_code = code
        registration_attempt.save()

    def send_letter_confirm_registration(self, data):
        html_body = render_to_string('confirmation_registration_email.html', data)
        msg = EmailMultiAlternatives(subject='Регистрация на сайте интернет-магазина TOP SHOP.', to=[data['email'], ])
        msg.attach_alternative(html_body, 'text/html')
        msg.send()


def validation_recaptcha_v2(request):
    recaptcha_response = request.POST.get('g-recaptcha-response')
    session = requests.session()
    request = session.post('https://www.google.com/recaptcha/api/siteverify', data={
        'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
        'response': recaptcha_response
    })
    result = json.loads(request.text)
    return result


class ActivateAccountView(View):
    def __init__(self):
        self.attempts = 3

    def get(self, request):
        if request.user.is_anonymous:
            account_activation_form = ActivationAccountForm()
            return render(request, 'activate_account.html', {'form': account_activation_form,
                                                             'GOOGLE_RECAPTCHA_SITE_KEY': settings.GOOGLE_RECAPTCHA_SITE_KEY})
        else:
            return redirect('home')

    # @validate_captcha    #не работает декоратор этот, пришлось вручную писать валидацию
    def post(self, request):
        account_activation_form = ActivationAccountForm(request.POST)
        if account_activation_form.is_valid():
            email = account_activation_form.cleaned_data['email']
            code = account_activation_form.cleaned_data['activation_code']
            if validation_recaptcha_v2(request):
                user_activation = RegistrationConfirmationByEmail.objects.get(email=email)

                if user_activation is not None and user_activation.activation_code == code:
                    user_activation.is_confirmed = True
                    user_activation.save()
                    return redirect('login')

                else:
                    self.attempts -= 1

                    if self.attempts <= 0:
                        return redirect('home')
            else:
                redirect('activate_account')

        return redirect('activate_account')


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


class ResetPasswordView(View):
    """
    Класс страницы сброса пароля, если пользователь забыл его
    """

    def get(self, request):
        if request.user.is_anonymous:
            reset_password_form = PasswordResetForm()
            return render(request, 'password_reset.html', {'form': reset_password_form})
        else:
            redirect('home')

    def post(self, request):
        reset_password_form = PasswordResetForm(request.POST)
        if reset_password_form.is_valid():
            associated_user = User.objects.get(email=reset_password_form.cleaned_data['email'])
            if associated_user.exists():
                subject = "Запрос сброса пароля"
                email_template_letter = "password_reset_email.html"
                main_info = {
                    "email": associated_user.email,
                    'domain': '127.0.0.1:8000',
                    'site_name': 'Online store on sofa TOP SHOP',
                    "uid": urlsafe_base64_encode(force_bytes(associated_user.pk)),
                    "user": associated_user,
                    'token': default_token_generator.make_token(associated_user),
                    'protocol': 'http',
                }
                email = render_to_string(email_template_letter, main_info)
                try:
                    send_mail(subject=subject, message=email,
                              from_email=settings.EMAIL_HOST, recipient_list=[associated_user.email],
                              fail_silently=False)
                except BadHeaderError:
                    return HttpResponse('Invalid header found.')
                return redirect('password_reset_done')
