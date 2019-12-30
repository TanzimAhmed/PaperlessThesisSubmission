from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('demo_editor/', views.demo_editor, name='demo_editor'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
]
