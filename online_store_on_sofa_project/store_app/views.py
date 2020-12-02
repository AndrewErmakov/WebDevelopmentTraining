from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from .models import Product, Rubric, Comment, Warehouse_products, Basket_user
from .forms import *


class HomePage(View):
    """Класс просмотра домашней страницы: на ней отображаются товары-новинки"""

    def get(self, request):
        new_products = Product.objects.all()[:6]
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
        try:
            count_product = Warehouse_products.objects.get(product=product).count_products
        except:
            count_product = 0

        try:
            presence_flag_comment_user = bool(len(product.comment_set.filter(author_comment=request.user)))
        except:
            presence_flag_comment_user = False

        try:
            total_rating = self.get_total_rating(product)
        except ZeroDivisionError:  # при отсутствии оценок от пользователей и комментариев на товар
            total_rating = 0

        context = {'product': product, 'rubrics': rubrics, 'presence_flag_comment_user': presence_flag_comment_user,
                   'rating': total_rating, 'count_product': count_product}
        return render(request, 'product_details.html', context)

    def get_total_rating(self, product, sum_points=0):
        comments = product.comment_set.all()
        for comment in comments:
            sum_points += comment.rating

        return round(sum_points / len(comments), 1)


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


class AddNewProductBySuperuser(View):
    """Класс добавления нового товара суперпользователем или манагерами магазина"""

    def get(self, request):
        if request.user.is_superuser or request.user.is_staff:
            form = AddNewProductBySuperuserForm()
            return render(request, 'add_new_product.html', {'form': form})
        else:
            return redirect('home')

    def post(self, request):
        form = AddNewProductBySuperuserForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return self.get(request)
        else:
            return redirect('home')


class AddImageProductBySuperuser(View):
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


class AddNewComment(LoginRequiredMixin, View):
    """Класс добавления комментария (мнения по товару, его оценка)"""

    def post(self, request):
        response_data = {}
        try:
            rating = request.POST.get('rating')
            text_comment = request.POST.get('text_comment')
            new_comment = Comment(
                rating=int(rating),
                text_comment=text_comment,
                author_comment=request.user,
                product=Product.objects.get(pk=request.POST.get('product_id'))
            )
            new_comment.save()
            response_data['status'] = 'OK'
            response_data['rating'] = rating
            response_data['text_comment'] = text_comment
            response_data['user'] = request.user.username
            return JsonResponse(response_data)

        except:
            response_data['status'] = 'BAD'
            return JsonResponse(response_data)


def custom_handler404(request, exception):
    return render(request, 'error404.html')


class AddProductToBasket(View, LoginRequiredMixin):
    def post(self, request):
        response_data = {}
        print(request.POST)
        try:
            product = Product.objects.get(pk=request.POST.get('product_id'))
            user = request.user
            new_product_to_buy = Basket_user(products=product, user=user)
            new_product_to_buy.save()
            response_data['status'] = 'OK'
            print(response_data['status'])
            return JsonResponse(response_data)
        except:
            response_data['status'] = 'BAD'
            print(response_data['status'])
            return JsonResponse(response_data)
