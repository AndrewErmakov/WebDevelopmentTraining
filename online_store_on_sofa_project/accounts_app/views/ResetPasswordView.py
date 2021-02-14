from django.conf import settings
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.views import View


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
