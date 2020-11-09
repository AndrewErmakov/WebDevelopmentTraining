from django.urls import path

from . import views

urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('activate_account/', views.ActivateAccountView.as_view(), name='activate_account'),
    path('change_password/', views.ChangePasswordView.as_view(), name='change_password'),
]