from django.urls import path

from . import views

# app_name = 'organizer'


urlpatterns = [
    path('', views.NotesListView.as_view(), name='home'),
    path('note/<int:pk>/', views.NoteDetailView.as_view(), name='details_note'),
    path('note/<int:pk>/add_participant/', views.AddParticipantToNote.as_view(), name='add_participant'),
    path('note/new/', views.NoteAddView.as_view(), name='add_new_note'),
    path('note/<int:pk>/edit/', views.NoteUpdateView.as_view(), name='note_edit'),
    path('note/<int:pk>/delete/', views.NoteDeleteView.as_view(), name='note_delete'),
    path('my_notes/', views.NotesListCurrentUserView.as_view(), name='notes_current_user'),
]
