from django.urls import path
from.views import dashboard, add_group

app_name = 'learners'
urlpatterns = [
    path('dashboard/', dashboard, name='dashboard'),
    path('groups/add/', add_group, name='add_group'),
]
