from django.shortcuts import render, redirect
from django.views import View
from rolepermissions.mixins import HasPermissionsMixin
from store_app.models import Product


class ChangeInfoProductView(View, HasPermissionsMixin):
    required_permission = 'change_info_existing_products'

    def get(self, request):
        try:
            products = Product.objects.all()
            return render(request, 'change_info_existing_products.html', {'products': products})
        except Exception as e:
            print(e)
            return redirect('home')

