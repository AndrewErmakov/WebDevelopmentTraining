from django.http import JsonResponse
from django.views import View
from rolepermissions.mixins import HasPermissionsMixin
from store_app.models import FeedBackWithClient
from django.core.mail import send_mail
from online_store_on_sofa_project.settings import EMAIL_HOST_USER


class SendAnswerToClientFeedbackRequest(HasPermissionsMixin, View):
    required_permission = 'feedback_with_clients'

    def post(self, request):
        response_data = {}
        try:
            request_feedback_id = int(request.POST.get('request_feedback_id'))
            text_answer = request.POST.get('text_answer')

            feedback_request = FeedBackWithClient.objects.get(id=request_feedback_id)
            feedback_request.given_feedback = True
            feedback_request.save()

            response_data['status'] = 'OK'

            send_mail(subject=f'Заявка на обратную связь №{request_feedback_id}',
                      message=text_answer,
                      from_email=EMAIL_HOST_USER,
                      recipient_list=[feedback_request.email_client])
            return JsonResponse(response_data)

        except Exception as e:
            print(e)
            response_data['status'] = 'BAD'
            return JsonResponse(response_data)
