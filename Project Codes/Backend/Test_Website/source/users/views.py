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
                return redirect('/')
        else:
            error = 'Username or Password Does Not match'
    context = {
        'form': form,
        'error': error
    }
    return render(request, 'users/login.html', context)


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
        form = RegistrationForm()
    return render(request, 'users/register.html', {'form': form})


def logout_user(request):
    logout(request)
    return redirect('/')
