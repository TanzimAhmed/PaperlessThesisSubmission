from django.urls import path
from .views import index, show, create, add_quiz, participate_quiz


app_name = 'classrooms'
urlpatterns = [
    path('', index, name='index'),
    path('<str:class_id>/show/', show, name='show'),
    path('create/', create, name='create'),
    path('<str:class_id>/quiz/add/', add_quiz, name='add_quiz'),
    path('<str:class_id>/quiz/participate/', participate_quiz, name='participate_quiz')
]
