from django.shortcuts import render, redirect
from django.views import View

from store_app.models import Product, Rubric


class ProductsBySortingView(View):
    """Класс просмотра страницы товарых отсортированных по какому-либо параметру"""

    def get(self, request, type_sorting):
        try:

            mapping_sort = {
                'increase_price': ['price', '1'],
                'decrease_price': ['-price', '2'],
                'top_rating': ['-avg_rating', '3'],
                'many_reviews': ['-count_reviews', '4']
            }

            products = Product.objects.all().order_by(mapping_sort[type_sorting][0])
            num_option = mapping_sort[type_sorting][1]

            rubrics = Rubric.objects.all()

            context = {'products': products, 'rubrics': rubrics, 'num_option': num_option}
            return render(request, 'sorted_products_page.html', context)
        except Exception as e:
            print(e)
            return redirect('add_image_product')