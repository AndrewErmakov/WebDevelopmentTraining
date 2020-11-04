from django.shortcuts import render
from django.views import View

from .models import Product, Rubric


class HomePage(View):
    """Класс просмотра домашней страницы: на ней отображаются товары-новинки"""

    def get(self, request):
        new_products = Product.objects.all()[:5]
        rubrics = Rubric.objects.all()
        context = {'new_products': new_products, 'rubrics': rubrics}
        return render(request, 'home.html', context)


class ContactsPage(View):
    """Класс просмотра страницы с контактами"""

    def get(self, request):
        return render(request, 'contacts.html')


class ProductDetailsPage(View):
    """Класс просмотра страницы - подробности о выбранном товаре"""

    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        rubrics = Rubric.objects.all()
        context = {'product': product, 'rubrics': rubrics}
        return render(request, 'product_details.html', context)


class ProductsByRubricPage(View):
    """Класс просмотра страницы товаров выбранной рубрики"""

    def get(self, request, pk):
        rubrics = Rubric.objects.all()
        selected_rubric = Rubric.objects.get(pk=pk)
        products = Product.objects.filter(rubric=selected_rubric)
        context = {'products': products,
                   'rubrics': rubrics,
                   'selected_rubric': selected_rubric}
        return render(request, 'products_by_rubric.html', context)
