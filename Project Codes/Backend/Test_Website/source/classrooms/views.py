from django.shortcuts import render, redirect, Http404
from django.http import JsonResponse
from .models import Classroom, Quiz
from .forms import CreateClassForm, QuizForm, QuestionForm
from project_paperless.utils import unique_id
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
    quiz_form = QuizForm(request.POST or None)
    if quiz_form.is_valid():
        quiz = quiz_form.save(commit=False)
        quiz.classroom = classroom
        quiz.save()
        return redirect('classrooms:show', class_id=class_id)
    quizzes = classroom.quiz.all()
    print(quizzes)
    context = {
        'classroom': classroom,
        'quizzes': quizzes,
        'quiz_form': quiz_form
    }
    return render(request, 'classrooms/show.html', context)


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


def show_quiz(request, class_id, quiz_id):
    try:
        classroom = request.user.classroom.get(id=class_id)
        quiz = classroom.quiz.get(id=quiz_id)
    except Classroom.DoesNotExist:
        raise Http404('Classroom Not found')
    except Quiz.DoesNotExist:
        raise Http404('Quiz Not found')
    print(quiz)
    question_form = QuestionForm(request.POST or None)
    if question_form.is_valid():
        question = question_form.save(commit=False)
        question.quiz = quiz
        question.save()
        return redirect('classrooms:show_quiz', class_id=class_id, quiz_id=quiz_id)
    questions = quiz.question.all()
    print(questions)
    context = {
        'classroom': classroom,
        'quiz': quiz,
        'questions': questions,
        'question_form': question_form
    }
    return render(request, 'classrooms/show_quiz.html', context)


def participate_quiz(request):
    quiz = Quiz.objects.last()
    performance = quiz.performance_set.get(student=request.user)
    print(performance)
    return render(request, 'classrooms/create.html')


def test_api(request):
    questions = [
        {
            'question': 'Which is your favourite animal?',
            'options': ['cat', 'dog', 'cow', 'goat'],
            'points': 1,
            'time': 60
        },
        {
            'question': 'Which is your favourite color?',
            'options': ['red', 'blue', 'green', 'orange'],
            'points': 1,
            'time': 60
        },
        {
            'question': 'Which is your favourite food?',
            'options': ['biriyani', 'tehari', 'khichuri', 'fried-rice'],
            'points': 1,
            'time': 60
        },
        {
            'question': 'Which is your favourite fruit?',
            'options': ['mango', 'orange', 'apple', 'banana'],
            'points': 1,
            'time': 60
        }
    ]
    return JsonResponse({'questions': questions})
