from django.urls import path
from.views import dashboard, add_group, request_submission

app_name = 'learners'
urlpatterns = [
    path('dashboard/', dashboard, name='dashboard'),
    path('groups/add/', add_group, name='add_group'),
    path('groups/request_submission/', request_submission, name='request_submission'),
]
