from django.urls import path
from.views import register, login_user, logout_user, dashboard, add_group

app_name = 'users'
urlpatterns = [
    path('login/', login_user, name='login'),
    path('register/', register, name='register'),
    path('logout/', logout_user, name='logout'),
    path('dashboard/', dashboard, name='dashboard'),
    path('groups/add/', add_group, name='add_group')
]
