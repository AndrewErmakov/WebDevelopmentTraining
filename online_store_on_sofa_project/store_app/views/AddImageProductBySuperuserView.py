from django.shortcuts import render, redirect
from django.views import View

from store_app.forms import AddImageNewProductBySuperuserForm


class AddImageProductBySuperuserView(View):
    """Класс добавления изображения нового товара суперпользователем или манагерами магазина"""

    def get(self, request):
        if request.user.is_superuser or request.user.is_staff:
            form = AddImageNewProductBySuperuserForm()
            return render(request, 'add_image_product.html', {'form': form})
        else:
            return redirect('home')

    def post(self, request):
        form = AddImageNewProductBySuperuserForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('add_image_product')
        else:
            return redirect('home')