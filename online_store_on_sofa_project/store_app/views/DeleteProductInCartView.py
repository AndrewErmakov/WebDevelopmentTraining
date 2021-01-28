from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views import View

from store_app.models import Product, ProductInCart, CartUser, WarehouseProducts


class DeleteProductInCartView(View, LoginRequiredMixin):
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