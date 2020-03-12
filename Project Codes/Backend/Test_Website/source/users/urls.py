from django.urls import path
from.views import RegistrationView, RegistrationConfirmView, VerificationView, LoginView, logout_user

app_name = 'users'
urlpatterns = [
    path('<str:user_type>/login/', LoginView.as_view(), name='login'),
    path('<str:user_type>/register/', RegistrationView.as_view(), name='register'),
    path('accounts/verify/', VerificationView.as_view(), name='verify'),
    path('<str:user_type>/registration/', RegistrationConfirmView.as_view(), name='registration'),
    path('logout/', logout_user, name='logout'),
]
