import json

import requests
from django.conf import settings


def validation_recaptcha_v2(request):
    recaptcha_response = request.POST.get('g-recaptcha-response')
    session = requests.session()
    request = session.post('https://www.google.com/recaptcha/api/siteverify', data={
        'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
        'response': recaptcha_response
    })
    result = json.loads(request.text)
    return result