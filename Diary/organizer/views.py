from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .models import DiaryNote


class NoteListView(ListView):
    """
    Класс просмотра всех записей в ежедневнике
    """
    model = DiaryNote
    template_name = 'home.html'
    queryset = DiaryNote.objects.all().order_by('date')[:10]


class NoteDetailView(DetailView):
    """
    Класс просмотра подробной инфы о выбранной записи в ежедневнике
    """

    def get(self, request, pk):
        note = DiaryNote.objects.get(pk=pk)
        return render(request, 'details_note.html', {'note': note})


class NoteAddView(CreateView):
    """
    Класс добавления новой записи в ежедневник
    """
    model = DiaryNote
    template_name = 'add_new_note.html'
    fields = '__all__'


class NoteUpdateView(UpdateView):
    """
    Класс обновления выбранной записи в ежедневнике
    """
    model = DiaryNote
    template_name = 'note_edit.html'
    fields = [
        'date',
        'note_heading',
        'text'
    ]


class NoteDeleteView(DeleteView):
    """
    Класс удаления выбранной записи в ежедневнике
    """
    model = DiaryNote
    template_name = 'note_delete.html'
    success_url = reverse_lazy('home')  # перенаправление на страницу home после того, как удаление выполнено
