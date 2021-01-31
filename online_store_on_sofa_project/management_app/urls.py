from django.urls import path

from .views import *

urlpatterns = [
    path('feedback_with_clients/', CheckRequestsFeedbackView.as_view(), name='feedback_with_clients'),
    path('response_to_request_feedback/', SendAnswerToClientFeedbackRequest.as_view(),
         name='response_to_request_feedback'),

]
