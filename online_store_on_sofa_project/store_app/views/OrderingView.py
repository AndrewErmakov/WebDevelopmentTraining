from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View

from store_app.coding_number_order import encryption_number_order
from store_app.models import Recipient, Order, ProductInCart, ProductsInOrder


class OrderingView(View, LoginRequiredMixin):
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
            return redirect('order_created',
                            encrypted_order_num=encryption_number_order(new_order.pk)[0],
                            key=encryption_number_order(new_order.pk)[1])
        except Exception as e:
            print(e)
            return redirect('user_cart_page')