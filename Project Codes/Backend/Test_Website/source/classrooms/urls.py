from django.urls import path
from .views import IndexView, ShowView, ShowQuizView, create, participate_quiz, test_api


app_name = 'classrooms'
urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('<str:class_id>/show/', ShowView.as_view(), name='show'),
    path('create/', create, name='create'),
    path('<str:class_id>/<str:quiz_id>/quiz/', ShowQuizView.as_view(), name='show_quiz'),
    path('<str:class_id>/quiz/participate/', participate_quiz, name='participate_quiz'),
    path('test/quiz/questions/', test_api, name='test_api')
]
