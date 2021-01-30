from django.http import Http404
from django.shortcuts import render


def error_404(request, exception=Http404):
    return render(request, '404.html', status=404)
