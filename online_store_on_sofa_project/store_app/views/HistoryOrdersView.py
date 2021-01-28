from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View

from store_app.models import Order


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