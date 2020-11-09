from captcha.fields import CaptchaField
from django import forms
from django.core import validators


class RegisterForm(forms.Form):
    username = forms.CharField(label='Никнейм', max_length=30, required=True)
    email = forms.EmailField(label='Электронная почта', min_length=3, max_length=40, required=True)
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(), min_length=6, max_length=20, required=True)
    repeat_password = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput(), min_length=6,
                                      max_length=20, required=True)
    first_name = forms.CharField(label='Ваше имя', max_length=20, min_length=2, required=True)
    last_name = forms.CharField(label='Ваша фамилия', max_length=30, required=True)


class LoginForm(forms.Form):
    username = forms.CharField(label='Никнейм', max_length=30, required=True)
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(), min_length=6, max_length=20, required=True)
    captcha = CaptchaField(label='Вы настоящий?')


class ActivationAccountForm(forms.Form):
    email = forms.EmailField(label='Электронная почта', min_length=3, max_length=40, required=True)
    activation_code = forms.CharField(label='Код активации', max_length=30, required=True,
                                      validators=[validators.MinLengthValidator(30)])


class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(label='Старый пароль', widget=forms.PasswordInput(), min_length=6, max_length=20,
                                   required=True)
    new_password = forms.CharField(label='Новый пароль', widget=forms.PasswordInput(), min_length=6, max_length=20,
                                   required=True)
