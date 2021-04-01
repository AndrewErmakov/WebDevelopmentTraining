from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Post(models.Model):
    title = models.CharField(max_length=50, verbose_name='Название поста')
    content = models.TextField(verbose_name='Текст поста')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время поста')
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return 'id:' + str(self.id) + ';' + self.title

    def get_absolute_url(self):
        """After creating new post"""
        return reverse('post_detail', args=[str(self.id)])
