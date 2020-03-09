from django.shortcuts import render, Http404
from .models import Classroom, Quiz
from .forms import CreateClassForm
from project_paperless.extras import unique_id
from datetime import date


# Create your views here.
def index(request):
    classrooms = request.user.classroom.all()
    print(classrooms)
    return render(request, 'classrooms/index.html', {'classrooms': classrooms})


def show(request, class_id):
    try:
        classroom = request.user.classroom.get(id=class_id)
    except Classroom.DoesNotExist:
        raise Http404('Classroom Not found')
    return render(request, 'classrooms/show.html', {'classroom': classroom})


def create(request):
    create_form = CreateClassForm(request.POST or None)
    if create_form.is_valid():
        class_id = unique_id(model=Classroom, length=4)
        classroom = create_form.save(commit=False)
        classroom.id = class_id
        course = create_form.cleaned_data['course'].split('.')
        classroom.course_code = course[0]
        classroom.section = course[1]
        classroom.instructor = request.user
        classroom.save()
    return render(request, 'classrooms/create.html', {'create_form': create_form})


def test_create(request):
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
