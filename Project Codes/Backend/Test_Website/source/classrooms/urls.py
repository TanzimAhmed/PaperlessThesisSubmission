from django.urls import path
from .views import IndexView, ShowView, ShowQuizView, UpdateQuizView, UpdateQuestionView, QuizView, \
    create, quiz_status, participate_quiz, test_api, join_class


app_name = 'classrooms'
urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('<str:class_id>/show/', ShowView.as_view(), name='show'),
    path('<str:class_id>/<str:quiz_id>/quiz/', ShowQuizView.as_view(), name='show_quiz'),
    path('join/', join_class, name='join_class'),
    path('create/', create, name='create'),
    path('<str:class_id>/<str:quiz_id>/quiz/update/', UpdateQuizView.as_view(), name='update_quiz'),
    path(
        '<str:class_id>/<str:quiz_id>/<str:question_id>/quiz/question/update/',
        UpdateQuestionView.as_view(),
        name='update_question'
    ),
    path('<str:class_id>/<str:quiz_id>/<str:status>/quiz/start', quiz_status, name='quiz_status'),
    path('<str:class_id>/<str:quiz_id>/quiz/participate/', participate_quiz, name='participate_quiz'),
    path('<str:class_id>/<str:quiz_id>/quiz/sit/', QuizView.as_view(), name='take_quiz'),
    path('test/quiz/questions/', test_api, name='test_api')
]
