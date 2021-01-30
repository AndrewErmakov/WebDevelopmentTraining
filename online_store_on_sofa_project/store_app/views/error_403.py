from django.core.exceptions import PermissionDenied
from django.shortcuts import render


def error_403(request, exception=PermissionDenied):
    return render(request, '403.html', status=403)
