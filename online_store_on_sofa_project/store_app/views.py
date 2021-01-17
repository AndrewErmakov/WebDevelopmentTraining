import random

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.views import View

from .forms import *
from .models import *


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
            count_product = WarehouseProducts.objects.get(product=product).count_products
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

        except Exception as e:
            print(e)
            response_data['status'] = 'BAD'
            return JsonResponse(response_data)


def custom_handler404(request, exception):
    return render(request, 'error404.html')


class AddProductToCart(View, LoginRequiredMixin):
    """Класс добавления товара в корзину пользователя"""

    def post(self, request):
        response_data = {}
        product_to_add_cart = Product.objects.get(pk=request.POST.get('product_id'))

        try:
            product_in_warehouse = WarehouseProducts.objects.get(product=product_to_add_cart)
            """Проверка если пользователь ввел число, превышающее кол-во товара на складе,
            если превышает, то страница остается без изменений, в корзину ничего не добавляется"""
            if product_in_warehouse.count_products < int(request.POST.get('count_product')):
                response_data['status'] = 'MORE'
                return JsonResponse(response_data)

            cart_current_user = CartUser.objects.filter(user=request.user)
            if len(cart_current_user) != 0:
                """Если корзина пользователя уже есть, и он добавлял ранее какой-то товар"""
                cart_current_user[0].products.add(product_to_add_cart)
                try:
                    """Если позиция данного товара уже в корзине и пользователь еще хочет добавить несколько товаров 
                    одной позиции """
                    product_in_cart = cart_current_user[0].productincart_set.get(product=product_to_add_cart)
                    product_in_cart.count_product_in_cart = product_in_cart.count_product_in_cart + \
                                                            int(request.POST.get('count_product'))
                    product_in_cart.save()

                except Exception as e:
                    print(e)
                    """В существующую корзину добавляется новый товар и указывается количество"""
                    cart_current_user[0].productincart_set.create(product=product_to_add_cart,
                                                                  count_product_in_cart=request.POST.get(
                                                                      'count_product'))

            else:
                """Иначе создается корзина, и добавляется первый товар в корзину"""
                cart_current_user = CartUser(user=request.user)
                cart_current_user.save()
                cart_current_user.products.add(Product.objects.get(pk=request.POST.get('product_id')))
                cart_current_user.productincart_set.create(product=product_to_add_cart,
                                                           count_product_in_cart=request.POST.get('count_product'))

            """Кол-во этого товара теперь на складе уменьшается"""

            product_in_warehouse.count_products -= int(request.POST.get('count_product'))
            product_in_warehouse.save()

            response_data['status'] = 'OK'
            return JsonResponse(response_data)
        except Exception as e:
            print(e)
            response_data['status'] = 'BAD'
            return JsonResponse(response_data)


class UserCartPage(View, LoginRequiredMixin):
    """Класс страницы просмотра корзины пользователя"""

    def get(self, request):
        try:
            cart_current_user = CartUser.objects.filter(user=request.user)
            if len(cart_current_user) != 0:
                cart_current_user = cart_current_user[0]
                products_in_cart = cart_current_user.products.all()
                count_each_product = {}
                total_sum = 0
                for product in products_in_cart:
                    product_in_cart = ProductInCart.objects.filter(cart_user=cart_current_user,
                                                                   product=product)[0]
                    count_each_product[product.pk] = [product_in_cart.count_product_in_cart]
                    count_each_product[product.pk].append(product_in_cart.count_product_in_cart * product.price)
                    total_sum += product_in_cart.count_product_in_cart * product.price
                return render(request, 'user_cart_page.html', {'products_in_cart': products_in_cart,
                                                               'is_empty_cart': False,
                                                               'count_each_product': count_each_product,
                                                               'total_sum': total_sum})
            else:
                return render(request, 'user_cart_page.html', {'is_empty_cart': True})
        except Exception as e:
            print(e)
            return render(request, 'user_cart_page.html')


class DeleteProductInCart(View, LoginRequiredMixin):
    """Удаление товара (только одной позиции!!!) из корзины"""

    def post(self, request):
        response_data = {}
        try:
            product = Product.objects.get(pk=request.POST.get('product_id'))

            """Удаление товара из таблицы CartUser"""
            request.user.cartuser.products.remove(product)

            """Удаление из таблицы ProductInCart"""
            ProductInCart.objects.get(cart_user=CartUser.objects.get(user=request.user),
                                      product=product).delete()

            """Восполнение запасов на складе данной позициии товара"""
            product_in_warehouse = WarehouseProducts.objects.get(product=product)
            product_in_warehouse.count_products += int(request.POST.get('count_products').split()[0])
            product_in_warehouse.save()

            response_data['status'] = 'OK'
            response_data['id'] = request.POST.get('product_id')
            return JsonResponse(response_data)

        except Exception as e:
            print(e)
            response_data['status'] = 'BAD'
            return JsonResponse(response_data)


class ReduceCountProducts(View, LoginRequiredMixin):
    """Уменьшение числа одной позиции товара в корзине на 1"""

    def post(self, request):
        response_data = {}
        try:
            product = Product.objects.get(pk=request.POST.get('product_id'))

            product_in_cart = ProductInCart.objects.get(cart_user=CartUser.objects.get(user=request.user),
                                                        product=product)

            if product_in_cart.count_product_in_cart == 1:
                response_data['status'] = 'знерщUGH'
                return JsonResponse(response_data)

            product_in_cart.count_product_in_cart -= 1
            product_in_cart.save()

            """Восполнение запасов на складе данной позициии товара"""
            product_in_warehouse = WarehouseProducts.objects.get(product=product)
            product_in_warehouse.count_products += 1
            product_in_warehouse.save()

            response_data['status'] = 'OK'
            response_data['id'] = request.POST.get('product_id')
            response_data['price'] = product.price
            return JsonResponse(response_data)

        except Exception as e:
            print(e)
            response_data['status'] = 'BAD'
            return JsonResponse(response_data)


class IncreaseCountProducts(View, LoginRequiredMixin):
    """Увеличение числа одной позиции товара в корзине на 1"""

    def post(self, request):
        response_data = {}
        try:
            product = Product.objects.get(pk=request.POST.get('product_id'))

            product_in_cart = ProductInCart.objects.get(cart_user=CartUser.objects.get(user=request.user),
                                                        product=product)

            """Проверка наличия еще 1 экземпляра товара"""
            product_in_warehouse = WarehouseProducts.objects.get(product=product)
            if product_in_warehouse.count_products >= 1:
                """Товар на складе есть"""
                product_in_cart.count_product_in_cart += 1
                product_in_cart.save()

                """Уменьшение запасов на складе данной позициии товара на 1"""
                product_in_warehouse.count_products -= 1
                product_in_warehouse.save()

                response_data['status'] = 'OK'
                response_data['id'] = request.POST.get('product_id')
                response_data['price'] = product.price

            else:
                """Товар на складе нет"""
                response_data['status'] = 'Not available'

            return JsonResponse(response_data)
        except Exception as e:
            print(e)
            response_data['status'] = 'BAD'
            return JsonResponse(response_data)


class Ordering(View, LoginRequiredMixin):
    def get(self, request):
        try:
            return render(request, 'ordering.html', {'user': request.user})
        except Exception as e:
            print(e)
            return redirect('home', {'need_warn': True})

    def post(self, request):
        try:
            new_recipient = Recipient.objects.create(name_recipient=request.POST.get('name_recipient'),
                                                     surname_recipient=request.POST.get('surname_recipient'),
                                                     phone_recipient=request.POST.get('phone'))
            new_order = Order.objects.create(recipient=new_recipient,
                                             buyer_email=request.user.email,
                                             payment_method=request.POST.get('payment_method'))
            new_order.num_order = str(new_order.pk).zfill(6)

            """Находим корзину пользователя и товары в ней"""
            cart_user = request.user.cartuser
            total_sum = 0
            for product in request.user.cartuser.products.all():
                product_in_cart = ProductInCart.objects.get(product=product, cart_user=cart_user)
                total_sum += product_in_cart.count_product_in_cart * product.price
                """Теперь сохраним товары в таблицу БД ProductsInOrder"""
                ProductsInOrder.objects.create(order=new_order,
                                               product=product,
                                               count_product_in_order=product_in_cart.count_product_in_cart)

                """Удалим товар из таблицы ProductsInCart"""
                product_in_cart.delete()

            new_order.total_sum = total_sum
            new_order.save()

            """Очистим таблицу пользователя"""
            cart_user.delete()

            """Закодируем наш номер заказа и передадим ему в url страницы о создании заказа"""
            encryption_key = random.randint(280, 570)
            print(encryption_key)
            encrypted_order_number = new_order.pk + encryption_key
            return redirect('order_created',
                            encrypted_order_num=encrypted_order_number,
                            key=encryption_key)
        except Exception as e:
            print(e)
            return redirect('user_cart_page')


class OrderCreatedView(View, LoginRequiredMixin):
    """Класс просмотра страницы о создании заказа"""

    def get(self, request, encrypted_order_num, key):
        try:
            decoded_order_number = str(encrypted_order_num - key).zfill(6)
            return render(request, 'order_created.html',
                          {'num': decoded_order_number})
        except Exception as e:
            print(e)
            return redirect('home')


class HistoryOrdersView(View, LoginRequiredMixin):
    """Класс просмотра истории заказов"""

    def get(self, request):
        """Получение истории страницы заказов"""
        try:
            orders = Order.objects.filter(buyer_email=request.user.email)
            return render(request, 'order_history_page.html',
                          {'orders': orders})
        except Exception as e:
            print(e)
            return redirect('home')




