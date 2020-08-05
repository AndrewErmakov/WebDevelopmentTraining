from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views import View

from .models import DiaryNote


class NotesListView(View):
    """
    Класс просмотра домашней страницы, если пользователь не авторизован,
    Или просмотр заметок пользователя, если он авторизован
    """

    def get(self, request):
        if request.user.is_authenticated:
            notes = DiaryNote.objects.filter(user=request.user).order_by('date')
            return render(request, 'notes_current_user.html', {'notes': notes})
        else:
            return render(request, 'home.html')


class NotesListCurrentUserView(View):
    """
    Класс просмотра своих записей после того, как пользователь авторизовался
    """

    def get(self, request):
        notes = DiaryNote.objects.filter(user=request.user).order_by('date')
        if request.user.is_authenticated:
            return render(request, 'notes_current_user.html', {'notes': notes})
        else:
            return redirect('login')


class NoteDetailView(View):
    """
    Класс просмотра подробной инфы о выбранной записи в ежедневнике
    """

    def get(self, request, pk):
        note = DiaryNote.objects.get(pk=pk)  # user=request.user
        if note.user == request.user:
            return render(request, 'details_note.html', {'note': note})
        else:
            return redirect('home')


class AddParticipantToNote(View):
    """Класс добавленния участника(ов) заметки"""

    def post(self, request, pk):
        note = DiaryNote.objects.get(pk=pk)
        name_participant = request.POST['participant']

        participant = User.objects.get(username=name_participant)
        note.participants.add(participant)
        note.save()
        return redirect('details_note', pk=pk)


class NoteAddView(View):
    """
    Класс добавления новой записи в ежедневник
    """

    def get(self, request):
        if request.user.is_authenticated:
            return render(request, 'add_new_note.html')
        else:
            return redirect('login')

    def post(self, request):
        date = request.POST['date']
        note_heading = request.POST['note_heading']
        text = request.POST['text']
        note = DiaryNote()

        note.user = request.user
        note.date = date
        note.note_heading = note_heading
        note.text = text

        note.save()

        return redirect('details_note',
                        pk=note.pk)  # перенаправление на страницу details_note после того, как добавили запись


class NoteUpdateView(View):
    """
    Класс обновления выбранной записи в ежедневнике
    """

    def get(self, request, pk):
        note = DiaryNote.objects.get(pk=pk)
        note.date = str(note.date)
        if note.user == request.user:
            return render(request, 'note_edit.html', {'note': note})
        else:
            return redirect('home')

    def post(self, request, pk):
        note = DiaryNote.objects.get(pk=pk)

        date = request.POST['date']
        note_heading = request.POST['note_heading']
        text = request.POST['text']
        note.date = date
        note.note_heading = note_heading
        note.text = text
        note.save()

        return redirect('details_note',
                        pk=note.pk)  # перенаправление на страницу details_note после того, как обновили запись


class NoteDeleteView(View):
    """
    Класс удаления выбранной записи в ежедневнике
    """

    def get(self, request, pk):
        note = DiaryNote.objects.get(pk=pk)
        if note.user == request.user:
            return render(request, 'note_delete.html', {'note': note})
        else:
            return redirect('home')

    def post(self, request, pk):
        note = DiaryNote.objects.get(pk=pk)
        note.delete()

        return redirect('home')  # перенаправление на страницу home после того, как удалили запись
