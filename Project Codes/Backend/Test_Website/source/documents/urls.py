from django.urls import path
from .views import upload_paper, show

app_name = 'documents'
urlpatterns = [
    path('upload/', upload_paper, name='upload_paper'),
    path('show/', show, name='show')
]
