from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView

from .models import DiaryNote


class NoteListView(ListView):
    model = DiaryNote
    template_name = 'home.html'
    queryset = DiaryNote.objects.all().order_by('date')[:10]


class NoteDetailView(DetailView):
    def get(self, request, pk):
        note = DiaryNote.objects.get(pk=pk)
        return render(request, 'details_note.html', {'note': note})


class NoteAddView(CreateView):
    model = DiaryNote
    template_name = 'add_new_note.html'
    fields = '__all__'
