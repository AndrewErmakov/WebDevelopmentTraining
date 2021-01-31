from django.shortcuts import render, redirect
from django.views import View
from rolepermissions.mixins import HasPermissionsMixin
from management_app.forms import AddImageForProductForm


class AddImagesForProductView(View, HasPermissionsMixin):
    required_permission = 'add_images_for_product'

    def get(self, request):
        try:
            form = AddImageForProductForm()
            return render(request, 'add_images_for_product.html', {'form': form})
        except Exception as e:
            print(e)
            return redirect('home')

    def post(self, request):
        try:
            form = AddImageForProductForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
            return redirect('add_images_for_product')

        except Exception as e:
            print(e)
            return redirect('home')
