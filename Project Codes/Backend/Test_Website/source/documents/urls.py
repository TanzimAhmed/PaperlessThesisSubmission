from django.urls import path
from .views import upload_paper, ShowView

app_name = 'documents'
urlpatterns = [
    path('upload/', upload_paper, name='upload_paper'),
    path('show/', ShowView.as_view(), name='show')
]
