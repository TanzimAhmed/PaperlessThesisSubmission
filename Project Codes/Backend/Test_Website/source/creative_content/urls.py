from django.urls import path
from . import views

app_name = 'creative_contents'
urlpatterns = [
    path('', views.index, name='index'),
    path('<str:link>/show/', views.show, name='content_display'),
    path('upload/', views.upload_file, name='upload_file'),
    path('demo_editor/', views.demo_editor, name='demo_editor'),
    path('editor/', views.editor, name='editor'),
]
