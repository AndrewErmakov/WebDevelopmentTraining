import datetime
import json

import pandas as pd
from django.shortcuts import render, redirect
from django.views import View
from rolepermissions.mixins import HasPermissionsMixin
from store_app.models import Order


class GetSalesAnalyticsView(View, HasPermissionsMixin):
    required_permission = 'get_analytics'

    def get(self, request):
        try:
            sold_products_for_period = {}

            today = datetime.datetime.today().date()
            date_first_order = Order.objects.order_by('created_at')[0].created_at.date()

            for date in pd.date_range(date_first_order, today):
                sold_products_for_period[str(date.date().strftime('%d.%m.%Y'))] = Order.objects.filter\
                        (created_at__date=date.date()).count()

            json_data = json.dumps([list(sold_products_for_period.keys()), list(sold_products_for_period.values())])
            return render(request, 'get_sales_analytics.html', {'sold_products_for_period': sold_products_for_period,
                                                                'json_data': json_data})
        except Exception as e:
            print(e)
            return redirect('home')
