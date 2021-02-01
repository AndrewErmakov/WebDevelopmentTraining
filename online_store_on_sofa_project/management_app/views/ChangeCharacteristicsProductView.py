from django.shortcuts import render, redirect
from django.views import View
from rolepermissions.mixins import HasPermissionsMixin
from store_app.models import Product


class ChangeCharacteristicsProductView(View, HasPermissionsMixin):
    required_permission = 'change_info_existing_products'

    def get(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)
            return render(request, 'change_characteristics_product.html', {'product': product})
        except Exception as e:
            print(e)
            return redirect('home')

    def post(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)
            product.title = request.POST.get('title')
            product.description = request.POST.get('description')
            product.price = request.POST.get('price')
            product.brand = request.POST.get('brand')
            product.save()
            return redirect('change_info_product')

        except Exception as e:
            print(e)
            return redirect('home')