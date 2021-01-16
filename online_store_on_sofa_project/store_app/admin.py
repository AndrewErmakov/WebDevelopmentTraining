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
    list_display = ('product', 'text_comment', 'author_comment', 'rating', 'date_comment')
    list_display_links = ['product', 'text_comment']
    search_fields = ('product', 'text_comment', 'author_comment', 'rating',)


class WarehouseProductsAdmin(admin.ModelAdmin):
    list_display = ('product', 'count_products')
    list_display_links = ['product', 'count_products']
    search_fields = ('product', 'count_products',)


class CartUserAdmin(admin.ModelAdmin):
    list_display = ['user']
    list_display_links = ['user']
    search_fields = ('products', 'user',)


class CountProductInCartAdmin(admin.ModelAdmin):
    list_display = ('product', 'count_product_in_cart', 'cart_user')
    list_display_links = ['product']
    search_fields = ('product', 'count_product_in_cart',)


class OrderAdmin(admin.ModelAdmin):
    list_display = ['num_order', 'created_at', 'recipient', 'buyer_email', 'total_sum', 'payment_method',
                    'method_receive_order', 'date_order']
    list_display_links = ['num_order', 'created_at', 'recipient', 'buyer_email', 'total_sum', 'payment_method',
                          'method_receive_order', 'date_order']
    search_fields = ('num_order', 'created_at', 'recipient', 'buyer_email', 'total_sum', 'payment_method',
                     'method_receive_order', 'date_order')


class RecipientAdmin(admin.ModelAdmin):
    list_display = ['name_recipient', 'surname_recipient', 'phone_recipient']
    list_display_links = ['name_recipient', 'surname_recipient', 'phone_recipient']
    search_fields = ('name_recipient', 'surname_recipient', 'phone_recipient',)


class CountProductInOrderAdmin(admin.ModelAdmin):
    list_display = ['product', 'count_product_in_order', 'order']
    list_display_links = ['product', 'count_product_in_order']
    search_fields = ('product', 'count_product_in_order', 'order')


admin.site.register(Product, ProductAdmin)
admin.site.register(Rubric)
admin.site.register(ImageProduct, ImageProductAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(WarehouseProducts, WarehouseProductsAdmin)
admin.site.register(CartUser, CartUserAdmin)
admin.site.register(ProductInCart, CountProductInCartAdmin)
admin.site.register(Recipient, RecipientAdmin)
admin.site.register(ProductsInOrder, CountProductInOrderAdmin)
admin.site.register(Order, OrderAdmin)
