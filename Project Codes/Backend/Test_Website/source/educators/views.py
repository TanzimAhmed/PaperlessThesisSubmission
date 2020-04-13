from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, Http404
from documents.forms import DocumentForm
from project_paperless.decorators import educator_required


# Create your views here.
@login_required(login_url='users:login')
def dashboard(request):
    # Fetching information
    groups = request.user.submission_group.all()
    classrooms = request.user.classroom.all()
    quizzes = []
    papers = []
    paper_requests = []
    for group in groups:
        if group.status == 'ACCEPTED':
            for paper in group.document.all():
                papers.append(paper)
        elif group.status == 'REQUESTED':
            paper_requests.append(group)
    for classroom in classrooms:
        for quiz in classroom.quiz.all():
            quizzes.append(quiz)

    context = {
        'classrooms': classrooms,
        'quizzes': quizzes,
        'groups': groups,
        'papers': papers,
        'paper_requests': paper_requests
    }
    print(context)
    return render(request, 'educators/dashboard.html', context)
