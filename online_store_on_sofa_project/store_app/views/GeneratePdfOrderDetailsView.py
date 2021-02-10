from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import FileResponse
from django.shortcuts import redirect
from django.views import View

from store_app.accessory_modules import GeneratePdfDetailsOrder
from store_app.models import Order


class GeneratePdfOrderDetailsView(View, LoginRequiredMixin):

    def get(self, request, num_str):
        """Данные, которые нужно записать в pdf"""
        try:
            order = Order.objects.get(num_order=num_str)
            generation_pdf = GeneratePdfDetailsOrder(order, num_str)
            result_pdf = generation_pdf.generate_pdf()

            return FileResponse(result_pdf, as_attachment=False, filename=f'Заказ №{num_str}.pdf')

        except Exception as e:
            print(e)
            return redirect('user_cart_page')
