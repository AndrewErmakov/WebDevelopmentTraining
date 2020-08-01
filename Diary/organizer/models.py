from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class DiaryNote(models.Model):
    """
    user - имя пользователя
    date - дата заметки (когда нужно что-то сделать)
    note_heading - заголовок заметки
    text - описание заметки
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    date = models.DateField()
    note_heading = models.CharField(max_length=155)
    text = models.TextField(default='Nothing')

    def __str__(self):
        """
        Строковое отображение модели
        """
        return self.note_heading


