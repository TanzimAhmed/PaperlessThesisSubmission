from django.urls import path
from . import views


urlpatterns = [
    path('', views.content_display, name='content_display'),
    path('<str:link>/show/', views.show, name='content_display'),
    path('demo_editor/', views.demo_editor, name='demo_editor'),
    path('editor/', views.editor, name='editor'),
]
