from django.shortcuts import render


def custom_handler404(request, exception):
    return render(request, 'error404.html')