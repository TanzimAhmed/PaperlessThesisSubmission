from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import RegistrationForm, LoginForm


def login_user(request):
    if request.user.is_authenticated:
        return redirect('/')
    form = LoginForm(request.POST or None)
    error = None
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


def logout_user(request):
    logout(request)
    messages.success(request, "You're Logged out SUCCESSFULLY")
    return redirect('/')
