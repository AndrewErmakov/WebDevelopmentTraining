from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import AnonymousUser
from django.http import JsonResponse
from django.views import View

from store_app.models import Product, WarehouseProducts, CartUser


class AddProductToCartView(View, LoginRequiredMixin):
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
            print(request.user == AnonymousUser)
            response_data['status'] = 'BAD'
            return JsonResponse(response_data)