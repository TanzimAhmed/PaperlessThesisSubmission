from django.core.mail import EmailMultiAlternatives
from django.contrib import messages
from django.shortcuts import render, redirect, Http404
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.template.loader import get_template
from .models import Verification
from .forms import StudentRegistrationForm, TeacherRegistrationForm, RegistrationForm, VerificationForm, LoginForm
from project_paperless.extras import UserAuthenticationViews, random_code


class RegistrationView(UserAuthenticationViews):
    student_template = teacher_template = 'users/registration.html'
    student_form_class = StudentRegistrationForm
    teacher_form_class = TeacherRegistrationForm
    email_html = 'emails/verification_email.html'
    email_text = 'emails/verification_email.txt'
    from_email = 'project.paperless20@gmail.com'
    email_subject = 'Test Verification Code'

    def student_form_valid(self):
        token = random_code()
        Verification.add_token(self.student_form.cleaned_data['username'], token)
        form = VerificationForm()
        return render(self.request, 'users/verification.html', {'form': form})

    def teacher_form_valid(self):
        print(self.teacher_form.cleaned_data['username'])
        return render(self.request, 'emails/verification_email.html', {'token': 1234})

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
    student_form_class = teacher_form_class = RegistrationForm

    def student_form_valid(self):
        user = self.student_form.save(commit=False)
        print(user)
        password = self.student_form.cleaned_data['password']
        user.set_password(password)
        user.save()
        messages.success(self.request, "Account created SUCCESSFULLY")
        return redirect('users:login')

    def teacher_form_valid(self):
        user = self.student_form.save(commit=False)
        print(user)
        password = self.student_form.cleaned_data['password']
        user.set_password(password)
        user.is_educator = True
        user.save()
        messages.success(self.request, "Account created SUCCESSFULLY")
        return redirect('users:login')


class LoginView(UserAuthenticationViews):
    student_template = teacher_template = 'users/login.html'
    student_form_class = teacher_form_class = LoginForm

    def student_form_valid(self):
        data = self.student_form.cleaned_data
        user = authenticate(username=data['username'], password=data['password'])
        if user is not None:
            if user.is_active:
                login(self.request, user)
                messages.success(self.request, "You're Logged in SUCCESSFULLY")
                return redirect('/')
        else:
            messages.error(self.request, 'Username or Password Does Not match')
            return self.student_view()

    def teacher_form_valid(self):
        data = self.teacher_form.cleaned_data
        user = authenticate(username=data['username'], password=data['password'])
        if user is not None:
            if user.is_active:
                login(self.request, user)
                messages.success(self.request, "You're Logged in SUCCESSFULLY")
                return redirect('/')
        else:
            messages.error(self.request, 'Username or Password Does Not match')
            return self.teacher_view()


class VerificationView(View):
    template = 'users/verification.html'

    def get(self, request):
        raise Http404('Page Not Found')

    def post(self, request):
        form = VerificationForm(request.POST)
        if form.is_valid():
            pass
        return render(request, self.template, {'form': form})


@login_required(login_url='/')
def logout_user(request):
    logout(request)
    messages.success(request, "You're Logged out SUCCESSFULLY")
    return redirect('/')
