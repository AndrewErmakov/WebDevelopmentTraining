from django.contrib.auth.models import User
from django.db import models


class DiaryNote(models.Model):
    """
    user - имя пользователя (создатель заметки)
    date - дата заметки (когда нужно что-то сделать)
    note_heading - заголовок заметки
    text - описание заметки
    participants - участники заметки
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='note_creator')
    date = models.DateField()
    note_heading = models.CharField(max_length=155)
    text = models.TextField(default='Nothing')
    participants = models.ManyToManyField(User, related_name='note_participants', default='')
    place = models.CharField(max_length=155, default='')

    def __str__(self):
        """
        Строковое отображение модели DiaryNote
        """
        return self.note_heading


