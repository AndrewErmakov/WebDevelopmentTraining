from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.models import User


# Create your views here.
class LoginView(View):
    def get(self, request):
        return render(request, 'login.html', {'prompt': 'Please login'})

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            print('Welcome')
            return redirect('home')
        else:
            print('Try to login again')
            return render(request, 'login.html', {'prompt': 'Try to login again'})


class SignUpView(View):
    def get(self, request):
        prompt = 'Welcome to the registration page'
        return render(request, 'signup.html', {'prompt': prompt})

    def post(self, request):
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password1']
        if self.is_form_valid(request):
            user = User.objects.create_user(username=username,
                                            email=email,
                                            password=password)
            user.save()
            return redirect('login')
        else:
            prompt = 'You are wrong, try again'
            return render(request, 'signup.html', {'prompt': prompt})

    def is_form_valid(self, request):
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if len(username) < 100 and password1 == password2 and '@' in email:
            return True
        else:
            return False
