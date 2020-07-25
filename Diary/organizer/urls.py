from django.urls import path

from . import views

# app_name = 'organizer'


urlpatterns = [
    path('', views.NoteListView.as_view(), name='home'),
    path('note/<int:pk>/', views.NoteDetailView.as_view(), name='details_note'),
    path('note/new/', views.NoteAddView.as_view(), name='add_new_note'),
    path('note/<int:pk>/edit/', views.NoteUpdateView.as_view(), name='note_edit'),
    path('note/<int:pk>/delete/', views.NoteDeleteView.as_view(), name='note_delete'),
]
