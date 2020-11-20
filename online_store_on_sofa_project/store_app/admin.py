from django.contrib import admin
from .models import Rubric, Product, ImageProduct


class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'price', 'sale_start_time', 'rubric')
    list_display_links = ('title', 'description')
    search_fields = ('title', 'description',)


class ImageProductAdmin(admin.ModelAdmin):
    list_display = ('product', 'image')
    list_display_links = ['product']
    search_fields = ('product',)


admin.site.register(Product, ProductAdmin)
admin.site.register(Rubric)
admin.site.register(ImageProduct, ImageProductAdmin)
