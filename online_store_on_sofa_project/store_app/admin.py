from django.contrib import admin
from .models import *


class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'price', 'sale_start_time', 'rubric')
    list_display_links = ('title', 'description')
    search_fields = ('title', 'description',)


class ImageProductAdmin(admin.ModelAdmin):
    list_display = ('product', 'image')
    list_display_links = ['product']
    search_fields = ('product',)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('product', 'text_comment', 'author_comment', 'rating', 'data_comment')
    list_display_links = ['product', 'text_comment']
    search_fields = ('product', 'text_comment',)


admin.site.register(Product, ProductAdmin)
admin.site.register(Rubric)
admin.site.register(ImageProduct, ImageProductAdmin)
admin.site.register(Comment, CommentAdmin)
