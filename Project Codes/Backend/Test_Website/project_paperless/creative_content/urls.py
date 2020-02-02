from django.urls import path
from . import views


urlpatterns = [
    path('demo_editor/', views.demo_editor, name='demo_editor')
]
