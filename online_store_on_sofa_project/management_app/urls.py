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
    path('change_info_product/', ChangeInfoProductView.as_view(), name='change_info_product'),

    path('add_count_received_product_to_warehouse/product/<int:pk>/', AddCountReceivedProductToWarehouse.as_view(),
         name='add_count_received_product_to_warehouse'),

    path('change_characteristics_product/product/<int:pk>/', ChangeCharacteristicsProductView.as_view(),
         name='change_characteristics_product'),

    path('get_analytics/sales/', GetSalesAnalyticsView.as_view(), name='get_sales_analytics'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
