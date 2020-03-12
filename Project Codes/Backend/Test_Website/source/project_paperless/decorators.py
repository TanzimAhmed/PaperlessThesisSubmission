from django.shortcuts import redirect
from django.contrib import messages


def anonymous_user(function):
    def wrapper_function(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/')
        return function(request, *args, **kwargs)
    return wrapper_function


def educator_required(function):
    def wrapper_function(request, *args, **kwargs):
        if not request.user.is_educator:
            messages.warning(request, "You do NOT have required permissions to view the content.")
            return redirect('/')
        return function(request, *args, **kwargs)
    return wrapper_function


def learner_required(function):
    def wrapper_function(request, *args, **kwargs):
        if request.user.is_educator:
            messages.warning(request, "You do NOT have required permissions to view the content.")
            return redirect('/')
        return function(request, *args, **kwargs)
    return wrapper_function
