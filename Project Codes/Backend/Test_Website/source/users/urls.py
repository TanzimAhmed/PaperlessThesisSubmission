from django.urls import path
from.views import RegistrationView, RegistrationConfirmView, VerificationView, LoginView, DashboardView, logout_user

app_name = 'users'
urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('<str:user_type>/register/', RegistrationView.as_view(), name='register'),
    path('accounts/verify/', VerificationView.as_view(), name='verify'),
    path('<str:user_type>/registration/', RegistrationConfirmView.as_view(), name='registration'),
]
