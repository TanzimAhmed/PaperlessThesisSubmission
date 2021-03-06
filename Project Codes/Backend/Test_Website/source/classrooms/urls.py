from django.urls import path
from .views import IndexView, ShowView, ShowQuizView, UpdateQuestionView, QuizView, GenerateGraphView, \
    create, quiz_status, participate_quiz, test_api, join_class, join_quiz


app_name = 'classrooms'
urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('<str:class_id>/show/', ShowView.as_view(), name='show'),
    path('<str:class_id>/<str:quiz_id>/quiz/', ShowQuizView.as_view(), name='show_quiz'),
    path('join/', join_class, name='join_class'),
    path('quiz/join/', join_quiz, name='join_quiz'),
    path('create/', create, name='create'),
    path(
        '<str:class_id>/<str:quiz_id>/<str:question_id>/quiz/question/update/',
        UpdateQuestionView.as_view(),
        name='update_question'
    ),
    path('quiz/stats/', GenerateGraphView.as_view(), name='show_quiz_stats'),
    path('<str:class_id>/<str:quiz_id>/<str:status>/quiz/status/', quiz_status, name='quiz_status'),
    path('<str:class_id>/<str:quiz_id>/quiz/participate/', participate_quiz, name='participate_quiz'),
    path('<str:class_id>/<str:quiz_id>/quiz/sit/', QuizView.as_view(), name='take_quiz'),
    path('test/quiz/questions/', test_api, name='test_api')
]
