from django.db import models
from django.urls import reverse


class DiaryNote(models.Model):
    """
    date - дата заметки (когда нужно что-то сделать)
    note_heading - заголовок заметки
    text - описание заметки
    """
    date = models.DateField()
    note_heading = models.CharField(max_length=155)
    text = models.TextField(default='Nothing')

    def __str__(self):
        """
        Строковое отображение модели
        """
        return self.note_heading

    def get_absolute_url(self):
        """
        После успешной отправки формы (добавление новой заметки в БД) пользователя отправляют на страницу details_note
        """
        return reverse('details_note', args=[str(self.pk)])

