import random
import string

from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.views import View

from accounts_app.forms import RegisterForm
from accounts_app.models import RegistrationConfirmationByEmail


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
                user = User.objects.create(username=username,
                                           email=email,
                                           password=password,
                                           first_name=first_name,
                                           last_name=last_name)

                secret_code = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits)
                                      for _ in range(30))
                self.save_registration_attempt(user=user, code=secret_code)

                data = {'email': email, 'first_name': first_name, 'last_name': last_name, 'code': secret_code}
                self.send_letter_confirm_registration(data)

                return redirect('activate_account')
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
