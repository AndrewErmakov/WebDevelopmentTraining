import datetime
from pprint import pprint

import pandas as pd
from django.shortcuts import render
from django.views import View
from rolepermissions.mixins import HasPermissionsMixin
from store_app.models import Order


class GetSalesAnalyticsView(View, HasPermissionsMixin):
    required_permission = 'get_analytics'

    def get(self, request):
        sold_products_for_period = {}

        today = datetime.datetime.today().date()
        date_first_order = Order.objects.order_by('created_at')[0].created_at.date()

        for date in pd.date_range(date_first_order, today):
            sold_products_for_period[date.date()] = Order.objects.filter(created_at__date=date.date()).count()

        return render(request, 'get_sales_analytics.html', {'sold_products_for_period': sold_products_for_period})
