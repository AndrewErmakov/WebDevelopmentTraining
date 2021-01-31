from django.urls import path
from django.conf.urls.static import static
from .views import *
from django.conf import settings


urlpatterns = [
    path('feedback_with_clients/', CheckRequestsFeedbackView.as_view(), name='feedback_with_clients'),
    path('response_to_request_feedback/', SendAnswerToClientFeedbackRequest.as_view(),
         name='response_to_request_feedback'),
    path('add_new_products/', AddNewProductsView.as_view(), name='add_new_products'),
    path('add_images_for_product/', AddImagesForProductView.as_view(), name='add_images_for_product'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
