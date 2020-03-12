from django.contrib import messages
from django.shortcuts import render, redirect
from .pages import CoverPage
from django.contrib.auth import authenticate, login, logout
from .pages import DocumentTest
from django.http import HttpResponse


def index(request):
    return render(request, 'pages/index.html')


def cover_page(request):
    allowed_range = range(1, 6)
    if request.method == 'POST' and request.POST['thesis_title'] is not None:
        print(request.POST)
        members = []
        for i in allowed_range:
            student_name = request.POST[f'name_{i}']
            student_id = request.POST[f'id_{i}']
            members.append({
                'name': student_name,
                'id': student_id
            })
        course_detail = request.POST['course'].split('.')
        cover_page = CoverPage(course_detail[0], course_detail[1], request.POST['thesis_title'],
                               request.POST['ins_name'], request.POST['group_name'], members)
        cover_page.generate_page()
        print("Page Generated")
        return redirect('/static/files/test_cover_page.docx')

    context = {'allowed_range': allowed_range}
    return render(request, 'pages/cover_page.html', context=context)


def demo_editor(request):
    return render(request, 'pages/demo_editor.html')


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
    return render(request, 'pages/login.html', context)
