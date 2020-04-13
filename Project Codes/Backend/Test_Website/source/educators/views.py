from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, Http404
from django.core.exceptions import PermissionDenied
from django.views import View
from django.utils.decorators import method_decorator
from documents.forms import DocumentForm
from learners.models import Group
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
    return render(request, 'educators/dashboard.html', context)


class PaperRequestView(View):
    def get(self, request):
        raise Http404('URL Not found')

    @method_decorator(login_required(login_url='users:login'))
    @method_decorator(educator_required)
    def post(self, request):
        if 'request_type' and 'group_id' in request.POST:
            request_type = request.POST['request_type']
            group_id = request.POST['group_id']
        else:
            raise PermissionDenied('Invalid request')
        try:
            group = request.user.submission_group.get(id=group_id)
        except Group.DoesNotExist:
            raise PermissionDenied('Group Not found')

        if request_type == 'accept':
            group.status = 'ACCEPTED'
            group.save()
            messages.success(request, f'Paper upload request has been Accepted for group: {group}')
        elif request_type == 'reject':
            group.status = 'IDLE'
            group.save()
            messages.warning(request, f'Paper upload request has been Rejected for group: {group}')
        return redirect('users:dashboard')
