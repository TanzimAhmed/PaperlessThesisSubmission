from django.shortcuts import render, redirect
from .cover_page import CoverPage
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


def login(request):
    return render(request, 'pages/login.html')


def register(request):
    return render(request, 'pages/register.html')


def test(request):
    return
