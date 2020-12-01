from django.contrib import admin
from .models import *


class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'price', 'sale_start_time', 'rubric')
    list_display_links = ('title', 'description')
    search_fields = ('title', 'description', 'price', 'rubric')


class ImageProductAdmin(admin.ModelAdmin):
    list_display = ('product', 'image')
    list_display_links = ['product']
    search_fields = ('product',)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('product', 'text_comment', 'author_comment', 'rating', 'data_comment')
    list_display_links = ['product', 'text_comment']
    search_fields = ('product', 'text_comment', 'author_comment', 'rating',)


class WarehouseProductsAdmin(admin.ModelAdmin):
    list_display = ('product', 'count_products')
    list_display_links = ['product', 'count_products']
    search_fields = ('product', 'count_products',)


class BasketUserAdmin(admin.ModelAdmin):
    list_display = ('products', 'user')
    list_display_links = ['products', 'user']
    search_fields = ('products', 'user',)


admin.site.register(Product, ProductAdmin)
admin.site.register(Rubric)
admin.site.register(ImageProduct, ImageProductAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Warehouse_products, WarehouseProductsAdmin)
admin.site.register(Basket_user, BasketUserAdmin)

