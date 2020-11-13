from django.conf import settings
from django.urls import path
from django.conf.urls.static import static
from .views import *
urlpatterns = [
    path('', HomePage.as_view(), name='home'),
    path('contacts/', ContactsPage.as_view(), name='contacts'),
    path('product_details/<int:pk>/', ProductDetailsPage.as_view(), name='product_details'),
    path('products_by_rubric/<int:pk>/', ProductsByRubricPage.as_view(), name='products_by_rubric'),
    path('add_new_product', AddNewProductBySuperuser.as_view(), name='add_new_product'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
