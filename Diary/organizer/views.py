from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .models import DiaryNote

from datetime import datetime

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


class NoteAddView(View):
    """
    Класс добавления новой записи в ежедневник
    """

    def get(self, request):
        return render(request, 'add_new_note.html')

    def post(self, request):
        date = request.POST['date']
        note_heading = request.POST['note_heading']
        text = request.POST['text']
        note = DiaryNote()
        note.date = date
        note.note_heading = note_heading
        note.text = text

        note.save()

        return redirect('details_note', pk=note.pk)


class NoteUpdateView(View):
    """
    Класс обновления выбранной записи в ежедневнике
    """

    def get(self, request, pk):
        note = DiaryNote.objects.get(pk=pk)
        note.date = str(note.date)
        return render(request, 'note_edit.html', {'note': note})

    def post(self, request, pk):
        note = DiaryNote.objects.get(pk=pk)

        date = request.POST['date']
        note_heading = request.POST['note_heading']
        text = request.POST['text']
        note.date = date
        note.note_heading = note_heading
        note.text = text
        note.save()

        return redirect('details_note', pk=note.pk)


class NoteDeleteView(DeleteView):
    """
    Класс удаления выбранной записи в ежедневнике
    """
    model = DiaryNote
    template_name = 'note_delete.html'
    success_url = reverse_lazy('home')  # перенаправление на страницу home после того, как удаление выполнено
