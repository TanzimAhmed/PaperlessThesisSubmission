from django.urls import path
from .views import index, create, add_quiz, participate_quiz


app_name = 'classrooms'
urlpatterns = [
    path('', index, name='index'),
    path('create/', create, name='create'),
    path('quiz/add/', add_quiz, name='add_quiz'),
    path('quiz/participate/', participate_quiz, name='participate_quiz')
]
