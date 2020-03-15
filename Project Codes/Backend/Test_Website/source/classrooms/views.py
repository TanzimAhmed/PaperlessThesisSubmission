from django.shortcuts import render, redirect, Http404
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views import View
from .models import Classroom, Quiz, Performance
from .forms import CreateClassForm, QuizForm, QuestionForm, JoinClassForm
from project_paperless.utils import unique_id, UserViews
from project_paperless.decorators import educator_required, learner_required


# Create your views here.
class IndexView(UserViews):
    student_template = 'classrooms/index.html'
    teacher_template = 'classrooms/index.html'

    def set_context(self, context=None):
        self.context = {'classrooms': self.request.user.classroom.all()}


class ShowView(UserViews):
    student_template = 'classrooms/learners/show.html'
    teacher_template = 'classrooms/educators/show.html'
    class_id = None

    @method_decorator(login_required(login_url='users:login'))
    def get(self, request, class_id):
        self.request = request
        self.class_id = class_id
        return self.user_view()

    @method_decorator(login_required(login_url='users:login'))
    @method_decorator(educator_required)
    def post(self, request, class_id):
        self.request = request
        return self.teacher_view()

    def student_view(self):
        classroom = self.get_classroom()
        quizzes = classroom.quiz.filter(is_open=True)
        print(quizzes)
        context = {
            'classroom': classroom,
            'quizzes': quizzes
        }
        return render(self.request, self.student_template, context)

    def teacher_view(self):
        classroom = self.get_classroom()
        quiz_form = QuizForm(self.request.POST or None)
        if quiz_form.is_valid():
            quiz = quiz_form.save(commit=False)
            quiz.classroom = classroom
            quiz.save()
            return redirect('classrooms:show', class_id=self.class_id)
        quizzes = classroom.quiz.all()
        context = {
            'classroom': classroom,
            'quizzes': quizzes,
            'quiz_form': quiz_form
        }
        return render(self.request, self.teacher_template, context)

    def get_classroom(self):
        try:
            classroom = self.request.user.classroom.get(id=self.class_id)
        except Classroom.DoesNotExist:
            raise Http404('Classroom Not found')
        return classroom


class ShowQuizView(UserViews):
    student_template = 'classrooms/learners/show_quiz.html'
    teacher_template = 'classrooms/educators/show_quiz.html'
    class_id = None
    quiz_id = None

    @method_decorator(login_required(login_url='users:login'))
    def get(self, request, class_id, quiz_id):
        self.request = request
        self.class_id = class_id
        self.quiz_id = quiz_id
        return self.user_view()

    @method_decorator(login_required(login_url='users:login'))
    @method_decorator(educator_required)
    def post(self, request, class_id, quiz_id):
        self.request = request
        self.class_id = class_id
        self.quiz_id = quiz_id
        return self.teacher_view()

    def student_view(self):
        quiz = self.get_quiz()
        if quiz.is_open:
            return render(self.request, self.student_template)
        questions = quiz.question.all()
        try:
            performance = quiz.performance_set.get(student=self.request.user)
        except Performance.DoesNotExist:
            answers = 'You didnot appear in the quiz'
        else:
            answers = performance.response
        context = {
            'quiz': quiz,
            'questions': questions,
            'answers': answers
        }
        return render(self.request, self.student_template, context)

    def teacher_view(self):
        quiz = self.get_quiz()
        question_form = QuestionForm(self.request.POST or None)
        if question_form.is_valid():
            question = question_form.save(commit=False)
            question.quiz = quiz
            question.save()
            return redirect('classrooms:show_quiz', class_id=self.class_id, quiz_id=self.quiz_id)
        questions = quiz.question.all()
        context = {
            'quiz': quiz,
            'questions': questions,
            'question_form': question_form
        }
        return render(self.request, self.teacher_template, context)

    def get_quiz(self):
        try:
            classroom = self.request.user.classroom.get(id=self.class_id)
            quiz = classroom.quiz.get(id=self.quiz_id)
        except Classroom.DoesNotExist:
            raise Http404('Classroom Not found')
        except Quiz.DoesNotExist:
            raise Http404('Quiz Not found')
        return quiz


class UpdateQuizView(View):
    template_name = 'classrooms/update.html'

    @method_decorator(login_required(login_url='users:login'))
    @method_decorator(educator_required)
    def get(self, request, class_id, quiz_id):
        quiz = self.get_quiz(class_id, quiz_id)
        form = QuizForm(instance=quiz)
        context = {
            'quiz': quiz,
            'form': form
        }
        return render(request, self.template_name, context)

    @method_decorator(login_required(login_url='users:login'))
    @method_decorator(educator_required)
    def post(self, request, class_id, quiz_id):
        quiz = self.get_quiz(class_id, quiz_id)
        form = QuizForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            quiz.title = data['title']
            quiz.due_date = data['due_date']
            quiz.is_open = data['is_open']
            quiz.save()
            return redirect('classrooms:show_quiz', class_id=class_id, quiz_id=quiz_id)
        context = {
            'quiz': quiz,
            'form': form
        }
        return render(request, self.template_name, context)

    def get_quiz(self, class_id, quiz_id):
        try:
            classroom = self.request.user.classroom.get(id=class_id)
            quiz = classroom.quiz.get(id=quiz_id)

        except Classroom.DoesNotExist:
            raise Http404('Classroom Not found')
        except Quiz.DoesNotExist:
            raise Http404('Quiz Not found')
        return quiz


class UpdateQuestionView(View):
    template_name = 'classrooms/update.html'

    @method_decorator(login_required(login_url='users:login'))
    @method_decorator(educator_required)
    def get(self, request, class_id, quiz_id, question_id):
        question = self.get_question(class_id, quiz_id, question_id)
        form = QuestionForm(instance=question)
        context = {
            'question': question,
            'form': form
        }
        return render(request, self.template_name, context)

    @method_decorator(login_required(login_url='users:login'))
    @method_decorator(educator_required)
    def post(self, request, class_id, quiz_id, question_id):
        question = self.get_question(class_id, quiz_id, question_id)
        form = QuestionForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            question.text = data['text']
            question.options = data['options']
            question.answer = data['answer']
            question.points = data['points']
            question.time = data['time']
            question.save()
            return redirect('classrooms:show_quiz', class_id=class_id, quiz_id=quiz_id)
        context = {
            'question': question,
            'form': form
        }
        return render(request, self.template_name, context)

    def get_question(self, class_id, quiz_id, question_id):
        try:
            classroom = self.request.user.classroom.get(id=class_id)
            quiz = classroom.quiz.get(id=quiz_id)
            question = quiz.question.get(id=question_id)
        except Classroom.DoesNotExist:
            raise Http404('Classroom Not found')
        except Quiz.DoesNotExist:
            raise Http404('Quiz Not found')
        return question


@login_required(login_url='users:login')
@educator_required
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


@login_required(login_url='users:login')
@educator_required
def quiz_status(request, class_id, quiz_id, status):
    if request.method == 'GET':
        raise Http404('Page Not Found')
    try:
        classroom = request.user.classroom.get(id=class_id)
        quiz = classroom.quiz.get(id=quiz_id)
    except Classroom.DoesNotExist:
        raise Http404('Classroom Not found')
    except Quiz.DoesNotExist:
        raise Http404('Quiz Not found')
    if status == 'start':
        quiz.is_running = True
        quiz.save()
    elif status == 'stop':
        quiz.is_running = False
        quiz.save()
    return redirect('classrooms:show_quiz', class_id=class_id, quiz_id=quiz_id)


@login_required(login_url='users:login')
@learner_required
def participate_quiz(request, class_id, quiz_id):
    try:
        classroom = request.user.classroom.get(id=class_id)
        quiz = classroom.quiz.get(id=quiz_id)
    except Classroom.DoesNotExist:
        raise Http404('Classroom Not found')
    except Quiz.DoesNotExist:
        raise Http404('Quiz Not found')
    performance = quiz.performance_set.get(student=request.user)
    print(performance)
    return render(request, 'classrooms/index.html')


@login_required(login_url='users:login')
def join_class(request):
    form = JoinClassForm(request.POST)
    if form.is_valid():
        try:
            classroom = Classroom.objects.get(id=form.cleaned_data['classroom'])
        except Classroom.DoesNotExist:
            raise Http404('Classroom Not Found')
        classroom.students.add(request.user)
        classroom.save()
    return render(request, 'classrooms/join.html', {'form': form})


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