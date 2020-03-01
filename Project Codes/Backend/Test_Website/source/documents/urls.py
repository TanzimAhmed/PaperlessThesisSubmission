from django.urls import path
from .views import upload_paper

app_name = 'documents'
urlpatterns = [
    path('upload/', upload_paper, name='upload_paper')
]
