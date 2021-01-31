from django.shortcuts import render
from django.views import View
from rolepermissions.mixins import HasPermissionsMixin
from store_app.models import FeedBackWithClient


class CheckRequestsFeedbackView(HasPermissionsMixin, View):
    required_permission = 'feedback_with_clients'

    def get(self, request):
        requests_for_feedback = FeedBackWithClient.objects.filter(given_feedback=False).order_by('id')
        context = {'requests': requests_for_feedback, 'username': request.user.username}
        return render(request, 'check_requests_for_feedback.html', context)

