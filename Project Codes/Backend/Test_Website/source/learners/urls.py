from django.urls import path
from.views import add_group

app_name = 'learners'
urlpatterns = [
    path('groups/add/', add_group, name='add_group'),
]
