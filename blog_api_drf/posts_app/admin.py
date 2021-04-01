from django.contrib import admin

from posts_app.models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'created', 'author')
    list_display_links = ('title',)
    search_fields = ('title', 'author')
    date_hierarchy = 'created'
