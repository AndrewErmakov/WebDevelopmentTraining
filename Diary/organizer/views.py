from django.views.generic import ListView, DetailView

from .models import DiaryNote


# Create your views here.


class NoteListView(ListView):
    model = DiaryNote
    template_name = 'home.html'
    queryset = DiaryNote.objects.all().order_by('date')[:10]


class NoteDetailView(DetailView):
    model = DiaryNote
    template_name = 'details_note.html'
