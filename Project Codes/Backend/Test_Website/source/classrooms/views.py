from django.shortcuts import render
from .models import Classroom, Quiz
from project_paperless.extras import unique_id
from datetime import date


# Create your views here.
def index(request):
    print(Classroom.objects.all())
    return render(request, 'classrooms/create.html')


def create(request):
    classroom = Classroom.objects.create(
        id=unique_id(model=Classroom, length=4),
        name='Class 1',
        course_code='CSE 499B',
        section='15',
        instructor=request.user
    )
    classroom.save()
    return render(request, 'classrooms/create.html')


def add_quiz(request):
    classroom = Classroom.objects.first()
    quiz = classroom.quiz.create(title='Quiz 2', due_date=date(2020, 3, 9))
    quiz.save()
    question = quiz.question.create(text='This is question 1', options='Mango, Orange, Banana', answer='apple')
    question.save()
    print(classroom.quiz.all())
    print(quiz.question.all())
    return render(request, 'classrooms/create.html')


def participate_quiz(request):
    quiz = Quiz.objects.last()
    performance = quiz.performance_set.get(student=request.user)
    print(performance)
    return render(request, 'classrooms/create.html')
