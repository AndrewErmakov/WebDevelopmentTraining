from datetime import datetime

import requests
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db.models.functions import ExtractYear, TruncMonth, ExtractMonth
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View

from .models import DiaryNote
from .secrets_organizer_app import api_key_ya_cards


class NotesListView(LoginRequiredMixin, View):
    """
    Класс просмотра домашней страницы, если пользователь не авторизован,
    Или просмотр заметок пользователя, если он авторизован
    """

    def get(self, request):
        return redirect('notes_current_user')


class NotesListCurrentUserView(LoginRequiredMixin, View):
    """
    Класс просмотра своих записей после того, как пользователь авторизовался
    """

    def get(self, request):
        today = datetime.today().date()

        created_notes = DiaryNote.objects.filter(user=request.user).annotate \
            (Year=ExtractYear('date')).annotate(month=ExtractMonth('date')).order_by('date')
        notes_as_participant = DiaryNote.objects.filter(participants=request.user).annotate \
            (Year=ExtractYear('date')).annotate(month=ExtractMonth('date')).order_by('date')

        return render(request, 'notes_current_user.html',
                      {'created_notes': created_notes,
                       'notes_as_participant': notes_as_participant,
                       'today': today})


class NoteDetailView(LoginRequiredMixin, View):
    """
    Класс просмотра подробной инфы о выбранной записи в ежедневнике
    """

    def get_response(self, address: str, api_key=api_key_ya_cards):
        main_response = requests.get(
            "https://geocode-maps.yandex.ru/1.x/",
            params=dict(format="json", apikey=api_key, geocode=address),
        )
        return main_response.json()['response']

    def get_coordinates(self, address) -> str:
        response = self.get_response(address)
        data = response['GeoObjectCollection']['featureMember']
        coordinates = data[0]['GeoObject']['Point']['pos']
        return coordinates

    def get(self, request, pk):
        note = DiaryNote.objects.get(pk=pk)  # user=request.user
        coordinates = self.get_coordinates(note.place)
        width = float(coordinates[1])
        longitude = float(coordinates[0])

        if note.user == request.user:
            return render(request, 'details_note.html', {
                'note': note,
                'alert_flag': False,
                'edit_flag': True,
                'width': width,
                'longitude': longitude})
        elif request.user in note.participants.all():
            return render(request, 'details_note.html', {
                'note': note,
                'alert_flag': False,
                'edit_flag': False,
                'width': width,
                'longitude': longitude})
        else:
            return redirect('home')


class AddParticipantToNote(LoginRequiredMixin, View):
    """Класс добавления участника(ов) заметки"""

    def post(self, request, pk):
        note = get_object_or_404(DiaryNote, pk=pk)
        name_participant = request.POST['participant']

        try:
            participant = User.objects.get(username=name_participant)
            note.participants.add(participant)
            note.save()
            return JsonResponse({'status': 'OK', 'name': name_participant})

        except User.DoesNotExist:

            return JsonResponse({'status': 'BAD', 'name': name_participant})


class NoteAddView(LoginRequiredMixin, View):
    """
    Класс добавления новой записи в ежедневник
    """

    def get(self, request):
        return render(request, 'add_new_note.html')

    def post(self, request):
        date = request.POST['date']
        note_heading = request.POST['note_heading']
        text = request.POST['text']
        place = request.POST['place']
        note = DiaryNote()

        note.user = request.user
        note.date = date
        note.note_heading = note_heading
        note.text = text
        note.place = place

        note.save()

        return redirect('details_note',
                        pk=note.pk)  # перенаправление на страницу details_note после того, как добавили запись


class NoteUpdateView(LoginRequiredMixin, View):
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


class NoteDeleteView(LoginRequiredMixin, View):
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
