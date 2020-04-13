from django.urls import path
from .views import PaperRequestView

app_name = 'educators'
urlpatterns = [
    path('process_request/', PaperRequestView.as_view(), name='process_request')
]
