from django.contrib.auth import logout
from django.shortcuts import redirect
from django.views import View


class LogoutView(View):
    """
    User logout
    """

    def get(self, request):
        logout(request)
        return redirect('home')