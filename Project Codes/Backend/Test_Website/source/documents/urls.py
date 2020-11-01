from django.urls import path
from .views import upload_paper, ShowView, check_document

app_name = 'documents'
urlpatterns = [
    path('upload/', upload_paper, name='upload_paper'),
    path('show/', ShowView.as_view(), name='show'),
    path('verify/', check_document, name='verify')
]
