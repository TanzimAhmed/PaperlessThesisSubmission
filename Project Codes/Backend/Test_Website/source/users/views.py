from django.core.mail import EmailMultiAlternatives
from django.urls import reverse
from django.contrib import messages
from django.shortcuts import render, redirect, Http404
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.template.loader import get_template
from educators.views import dashboard as teacher_dashboard
from learners.views import dashboard as learner_dashboard
from .models import Verification
from .forms import StudentRegistrationVerificationForm, TeacherRegistrationVerificationForm, \
    StudentRegistrationForm, TeacherRegistrationForm, VerificationForm, LoginForm
from project_paperless.utils import UserAuthenticationViews, UserViews, random_code, fetch_email_address


class RegistrationView(UserAuthenticationViews):
    student_template = teacher_template = 'users/registration.html'
    student_form_class = StudentRegistrationVerificationForm
    teacher_form_class = TeacherRegistrationVerificationForm
    email_html = 'emails/verification_email.html'
    email_text = 'emails/verification_email.txt'
    from_email = 'project.paperless20@gmail.com'
    email_subject = 'Test Verification Code'

    def student_form_valid(self):
        token = random_code()
        print(token)
        student_id = self.student_form.cleaned_data['username']
        Verification.add_token(student_id, token)
        email_address = f'{student_id}@northsouth.edu'
        # self.send_verification_email(email_address, token)
        form = VerificationForm(initial={'username': student_id})
        messages.success(self.request, 'A Verification Code has been sent to your North South email address.')
        return render(self.request, 'users/verification.html', {'form': form})

    def teacher_form_valid(self):
        token = random_code()
        print(token)
        data = self.teacher_form.cleaned_data
        email_address = fetch_email_address(data['department'], data['username'])
        print(email_address)
        Verification.add_token(email_address, token)
        form = VerificationForm(initial={'username': email_address})
        messages.success(self.request, 'A Verification Code has been sent to your North South email address.')
        return render(self.request, 'users/verification.html', {'form': form})

    def send_verification_email(self, to_email, token):
        html = get_template(self.email_html)
        text = get_template(self.email_text)

        text_content = text.render({'token': token})
        html_content = html.render({'token': token})
        email = EmailMultiAlternatives(self.email_subject, text_content, self.from_email, [to_email])
        email.attach_alternative(html_content, "text/html")
        email.send(fail_silently=False)


class RegistrationConfirmView(UserAuthenticationViews):
    student_template = teacher_template = 'users/register.html'
    student_form_class = StudentRegistrationForm
    teacher_form_class = TeacherRegistrationForm

    def get(self, request, user_type):
        raise Http404('Page Not Found')

    def student_form_valid(self):
        token = self.student_form.cleaned_data['verification_code']
        user = self.student_form.save(commit=False)
        try:
            verification = Verification.objects.get(username=user.username)
        except Verification.DoesNotExist:
            messages.error(self.request, 'Invalid Verification Code')
        else:
            if verification.check_token(token) and not verification.is_educator:
                password = self.student_form.cleaned_data['password']
                user.set_password(password)
                user.email = f'{user.username}@northsouth.edu'
                user.save()
                verification.delete()
                messages.success(self.request, "Account created SUCCESSFULLY")
            else:
                messages.error(self.request, 'Invalid Verification Code')
            return redirect('users:login')
        return self.student_view()

    def teacher_form_valid(self):
        token = self.teacher_form.cleaned_data['verification_code']
        user = self.teacher_form.save(commit=False)
        try:
            verification = Verification.objects.get(username=user.email)
        except Verification.DoesNotExist:
            messages.error(self.request, 'Invalid Verification Code')
        else:
            if verification.check_token(token) and not verification.is_educator:
                password = self.student_form.cleaned_data['password']
                user.set_password(password)
                user.is_educator = True
                user.save()
                verification.delete()
                messages.success(self.request, "Account created SUCCESSFULLY")
            else:
                messages.error(self.request, 'Invalid Verification Code')
            return redirect('users:login')
        return self.teacher_view()


class LoginView(View):
    template_name = 'users/login.html'
    form = None
    request = None

    def get(self, request):
        self.request = request
        self.form = LoginForm()
        return self.default_view()

    def post(self, request):
        self.request = request
        self.form = LoginForm(request.POST)
        if self.form.is_valid():
            data = self.form.cleaned_data
            return self.valid_form(data)

    def valid_form(self, data):
        user = authenticate(username=data['username'], password=data['password'])
        if user is not None:
            if user.is_active:
                login(self.request, user)
                messages.success(self.request, "You're Logged in SUCCESSFULLY")
                return redirect('/')
        else:
            messages.error(self.request, 'Username or Password Does Not match')
            return self.default_view()

    def default_view(self):
        return render(self.request, self.template_name, {'form': self.form})


class DashboardView(UserViews):

    def teacher_view(self):
        return teacher_dashboard(self.request)

    def student_view(self):
        return learner_dashboard(self.request)


class VerificationView(View):
    template = 'users/verification.html'

    def get(self, request):
        raise Http404('Page Not Found')

    def post(self, request):
        form = VerificationForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            try:
                verification = Verification.objects.get(username=data['username'])
            except Verification.DoesNotExist:
                messages.error(request, 'Invalid Verification Code')
            else:
                if verification.check_token(data['code']):
                    if verification.is_educator:
                        form = TeacherRegistrationForm(initial={'email': data['username']})
                        register_url = reverse('users:registration', args=['teacher'])
                    else:
                        form = StudentRegistrationForm(initial={'username': data['username']})
                        register_url = reverse('users:registration', args=['student'])
                    verification.update_time()
                    context = {
                        'form': form,
                        'register_url': register_url
                    }
                    return render(request, 'users/register.html', context)
                else:
                    messages.error(request, 'Invalid Verification Code')
        return render(request, self.template, {'form': form})


@login_required(login_url='users:login')
def logout_user(request):
    logout(request)
    messages.success(request, "You're Logged out SUCCESSFULLY")
    return redirect('/')
