from django.urls import path
from.views import RegistrationView, RegistrationConfirmView, VerificationView, LoginView, logout_user

app_name = 'users'
urlpatterns = [
    path('<str:user_type>/login/', LoginView.as_view(), name='login'),
    path('<str:user_type>/register/', RegistrationView.as_view(), name='register'),
    path('accounts/verify/', VerificationView.as_view(), name='verify'),
    path('<str:user_type>/register/confirm/', RegistrationConfirmView.as_view(), name='confirm'),
    path('logout/', logout_user, name='logout'),
]
