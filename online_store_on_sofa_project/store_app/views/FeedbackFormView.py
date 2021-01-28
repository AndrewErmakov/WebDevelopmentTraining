from django.http import JsonResponse
from django.views import View

from store_app.models import FeedBackWithClient


class FeedbackFormView(View):
    """Класс обработки отправки данных на заявку по получению обратной связи"""

    def post(self, request):
        response_data = {}
        try:
            FeedBackWithClient.objects.create(
                name_client=request.POST.get('name'),
                phone_client=request.POST.get('phone'),
                email_client=request.POST.get('email'),
                question_client=request.POST.get('question')
            )
            response_data['status'] = 'OK'

        except Exception as e:
            print(e)
            response_data['status'] = 'BAD'

        return JsonResponse(response_data)