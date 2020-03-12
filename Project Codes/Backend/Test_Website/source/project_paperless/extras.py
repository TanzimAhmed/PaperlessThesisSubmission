from django.views import View
from django.shortcuts import render
from django.utils.decorators import method_decorator
import random
import string
from django.utils.timezone import datetime
from .decorators import anonymous_user, educator_required, learner_required


COURSE_CHOICE_LIST = [
    ('CSE 499A.21', 'CSE 499A, Section 21'),
    ('CSE 499B.15', 'CSE 499B, Section 15'),
]

year = datetime.now().year

SEMESTER_CHOICE_LIST = [
    (f'SP_{year}', f'Spring {year}'),
    (f'SM_{year}', f'Summer {year}'),
    (f'FL_{year}', f'Fall {year}'),
]


class UserAuthenticationViews(View):
    student_template = None
    teacher_template = None
    student_form_class = None
    teacher_form_class = None
    student_form_initial = None
    teacher_form_initial = None
    student_form = None
    teacher_form = None
    request = None

    @method_decorator(anonymous_user)
    def get(self, request, user_type):
        self.request = request
        return self.user_view(user_type)

    @method_decorator(anonymous_user)
    def post(self, request, user_type):
        self.request = request
        return self.user_view(user_type)

    def user_view(self, user_type):
        if user_type.lower() == 'student':
            self.student_form = self.student_form_class(self.request.POST or None, initial=self.student_form_initial)
            if self.student_form.is_valid():
                return self.student_form_valid()
            return self.student_view()
        elif user_type.lower() == 'teacher':
            self.teacher_form = self.teacher_form_class(self.request.POST or None, initial=self.teacher_form_initial)
            if self.teacher_form.is_valid():
                return self.teacher_form_valid()
            return self.teacher_view()

    def student_form_valid(self):
        pass

    def teacher_form_valid(self):
        pass

    def student_view(self):
        return render(self.request, self.student_template, {'form': self.student_form})

    def teacher_view(self):
        return render(self.request, self.teacher_template, {'form': self.teacher_form})


def unique_id(model, target_column='id', length=8):
    """Random String Generator"""
    temp_link = random_string(length)
    try:
        model.objects.get(**{target_column: temp_link})
    except model.DoesNotExist:
        return temp_link
    else:
        return unique_id(model=model, target_column=target_column)


def random_string(string_length):
    """Generate a random string of letters and digits """
    letters_and_digits = string.ascii_letters + string.digits
    return ''.join(random.choice(letters_and_digits) for i in range(string_length))


def random_code(length=5):
    digits = string.digits
    return ''.join(random.choice(digits) for i in range(length))


"""
@anonymous_user
def register(request):
    form = RegistrationForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        print(user)
        password = form.cleaned_data['password']
        user.set_password(password)
        user.save()
        messages.success(request, "Account created SUCCESSFULLY")
        return redirect('users:login')
    return render(request, 'users/register.html', {'form': form})


@anonymous_user
def login_user(request):
    form = LoginForm(request.POST or None)
    if form.is_valid():
        data = form.cleaned_data
        user = authenticate(username=data['username'], password=data['password'])
        if user is not None:
            if user.is_active:
                login(request, user)
                messages.success(request, "You're Logged in SUCCESSFULLY")
                return redirect('/')
        else:
            messages.error(request, 'Username or Password Does Not match')
    return render(request, 'users/login.html', {'form': form})
"""
