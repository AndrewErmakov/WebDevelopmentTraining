from django.urls import path
from .views import HomePage, ContactsPage, ProductDetailsPage, ProductsByRubricPage
urlpatterns = [
    path('', HomePage.as_view(), name='home'),
    path('contacts/', ContactsPage.as_view(), name='contacts'),
    path('product_details/<int:pk>/', ProductDetailsPage.as_view(), name='product_details'),
    path('products_by_rubric/<int:pk>/', ProductsByRubricPage.as_view(), name='products_by_rubric')
]
