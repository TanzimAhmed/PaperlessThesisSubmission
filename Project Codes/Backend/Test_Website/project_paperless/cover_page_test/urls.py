from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('demo_editor/', views.demo_editor, name='demo_editor'),
]
