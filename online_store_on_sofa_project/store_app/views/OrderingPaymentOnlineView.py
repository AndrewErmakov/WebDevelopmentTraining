import stripe
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View
from online_store_on_sofa_project.secrets import STRIPE_APIKEY
from store_app.accessory_modules import encryption_number_order
from store_app.models import Recipient, Order, ProductInCart, ProductsInOrder


class OrderingPaymentOnlineView(View, LoginRequiredMixin):
    def get(self, request):
        try:
            total_sum = 0
            for product_in_cart in ProductInCart.objects.filter(cart_user__user=request.user):
                total_sum += product_in_cart.product.price * product_in_cart.count_product_in_cart

            stripe.api_key = STRIPE_APIKEY
            intent = stripe.PaymentIntent.create(
                amount=int(total_sum * 100),
                currency='rub',
                metadata={'integration_check': 'accept_a_payment'}
            )

            return render(request, 'ordering_payment_online.html', {'user': request.user,
                                                                    'client_secret': intent.client_secret})
        except Exception as e:
            print(e)
            return redirect('home')

    def post(self, request):
        try:
            new_recipient = Recipient.objects.create(name_recipient=request.POST.get('name_recipient'),
                                                     surname_recipient=request.POST.get('surname_recipient'),
                                                     phone_recipient=request.POST.get('phone'))
            new_order = Order.objects.create(recipient=new_recipient,
                                             buyer_email=request.user.email,
                                             payment_method='Онлайн')
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
            encrypt_num_order = encryption_number_order(new_order.pk)

            return redirect('order_created',
                            encrypted_order_num=encrypt_num_order['encrypted_order_number'],
                            key=encrypt_num_order['encryption_key'])

        except Exception as e:
            print(e)
            return redirect('user_cart_page')
