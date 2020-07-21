from django.db import models


# Create your models here.
class DiaryNote(models.Model):
    date = models.DateField()
    note_heading = models.CharField(max_length=155)
    text = models.TextField(default='Nothing')

    def __str__(self):
        """
        Строковое отображение модели
        """
        return self.note_heading
