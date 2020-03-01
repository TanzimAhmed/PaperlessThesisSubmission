from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('test_page/', views.test, name='test'),
    path('cover_page/', views.cover_page, name='cover_page'),
]
