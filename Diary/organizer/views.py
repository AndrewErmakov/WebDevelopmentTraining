from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View

from .models import DiaryNote


class NotesListView(View):
    """
    Класс просмотра домашней страницы, если пользователь не авторизован,
    Или просмотр заметок пользователя, если он авторизован
    """

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('notes_current_user')
        else:
            return render(request, 'home.html')


class NotesListCurrentUserView(View):
    """
    Класс просмотра своих записей после того, как пользователь авторизовался
    """

    def get(self, request):
        if request.user.is_authenticated:
            created_notes = DiaryNote.objects.filter(user=request.user).order_by('date')
            notes_as_participant = DiaryNote.objects.filter(participants=request.user).order_by('date')
            return render(request, 'notes_current_user.html', {
                'created_notes': created_notes,
                'notes_as_participant': notes_as_participant})
        else:
            return redirect('login')


class NoteDetailView(View):
    """
    Класс просмотра подробной инфы о выбранной записи в ежедневнике
    """

    def get(self, request, pk):
        note = DiaryNote.objects.get(pk=pk)  # user=request.user
        if note.user == request.user:
            return render(request, 'details_note.html', {'note': note, 'alert_flag': False, 'edit_flag': True})
        elif request.user in note.participants.all():
            return render(request, 'details_note.html', {'note': note, 'alert_flag': False, 'edit_flag': False})
        else:
            return redirect('home')


class AddParticipantToNote(View):
    """Класс добавления участника(ов) заметки"""

    def post(self, request, pk):
        note = get_object_or_404(DiaryNote, pk=pk)
        name_participant = request.POST['participant']

        try:
            participant = User.objects.get(username=name_participant)
            note.participants.add(participant)
            note.save()
            return redirect('details_note', pk=pk)
        except User.DoesNotExist:
            return render(request, 'details_note.html', {'note': note, 'alert_flag': True, 'edit_flag': True})


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
