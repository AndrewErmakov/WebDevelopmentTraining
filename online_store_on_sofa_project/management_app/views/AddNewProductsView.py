from django.shortcuts import render, redirect
from django.views import View
from rolepermissions.mixins import HasPermissionsMixin
from management_app.forms import AddNewProductsForm
from store_app.models import Product, WarehouseProducts


class AddNewProductsView(View, HasPermissionsMixin):
    required_permission = 'add_products'

    def get(self, request):
        try:
            form = AddNewProductsForm()
            return render(request, 'add_new_products.html', {'form': form})
        except Exception as e:
            print(e)
            return redirect('home')

    def post(self, request):
        try:
            form = AddNewProductsForm(request.POST)

            if form.is_valid():
                new_product = Product.objects.create(
                    title=form.cleaned_data['title'],
                    description=form.cleaned_data['description'],
                    price=form.cleaned_data['price'],
                    brand=form.cleaned_data['brand'],
                    rubric=form.cleaned_data['rubric']
                )
                WarehouseProducts.objects.create(
                    product=new_product,
                    count_products=request.POST.get('count_product')
                )
            return redirect('add_images_for_product')

        except Exception as e:
            print(e)
            return redirect('home')
