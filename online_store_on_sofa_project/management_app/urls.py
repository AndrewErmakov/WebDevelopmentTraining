from django.urls import path

from .views import *

urlpatterns = [
    path('feedback_with_clients/', CheckRequestsFeedbackView.as_view(), name='feedback_with_clients'),

]
