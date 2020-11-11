from django.contrib import admin
from .models import Rubric, Product


class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'price', 'sale_start_time', 'rubric', 'image_product')
    list_display_links = ('title', 'description')
    search_fields = ('title', 'description',)


admin.site.register(Product, ProductAdmin)
admin.site.register(Rubric)
