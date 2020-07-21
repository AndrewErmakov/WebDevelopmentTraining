from django.urls import path

from . import views

app_name = 'organizer'


urlpatterns = [
    path('', views.NoteListView.as_view(), name='home'),
    path('note/<int:pk>/', views.NoteDetailView.as_view(), name='details_note'),
]
