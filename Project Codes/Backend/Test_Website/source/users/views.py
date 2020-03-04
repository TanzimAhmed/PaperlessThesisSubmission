from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import RegistrationForm, LoginForm, CreateGroupForm, GroupSelectForm
from .models import Group, User


def register(request):
    if request.user.is_authenticated:
        return redirect('/')
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


def login_user(request):
    if request.user.is_authenticated:
        return redirect('/')
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


def logout_user(request):
    logout(request)
    messages.success(request, "You're Logged out SUCCESSFULLY")
    return redirect('/')


def dashboard(request):
    groups_form = GroupSelectForm()
    groups_form.update_choice(request.user)
    return render(request, 'users/dashboard.html', {'groups_form': groups_form})


def add_group(request):
    group_form = CreateGroupForm(request.POST or None)
    group_form.set_user(request.user.username)
    if group_form.is_valid():
        group = group_form.save(commit=False)
        cleaned_data = group_form.cleaned_data
        course = cleaned_data['course'].split('.')
        group.course_code = course[0]
        group.section = course[1]
        group.upload = False
        group.save()
        group.members.add(request.user)
        for member in cleaned_data['members']:
            group.members.add(member)
        print(group.members.all())
    return render(request, 'users/_dashboard.html', {'group_form': group_form})
