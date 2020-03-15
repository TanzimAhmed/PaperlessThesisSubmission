from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, Http404
from documents.forms import DocumentForm
from classrooms.forms import JoinClassForm
from project_paperless.decorators import learner_required
from .forms import CreateGroupForm, GroupSelectForm
from .models import Group


# Create your views here.
@login_required(login_url='users:login')
def dashboard(request):
    # Fetching information
    groups = request.user.group_set.all()
    classrooms = request.user.classroom.all()
    papers = []
    for group in groups:
        papers.append(group.document.all())

    # Creating forms
    groups_form = GroupSelectForm()
    groups_form.update_choice(request.user)
    class_form = JoinClassForm()

    context = {
        'classrooms': classrooms,
        'groups': groups,
        'papers': papers,
        'groups_form': groups_form,
        'class_form': class_form
    }
    return render(request, 'learners/dashboard.html', context)


@login_required(login_url='users:login')
@learner_required
def add_group(request):
    group_form = CreateGroupForm(request.POST or None)
    group_form.set_user(request.user.username)
    if group_form.is_valid():
        group = group_form.save(commit=False)
        cleaned_data = group_form.cleaned_data
        course = cleaned_data['course'].split('.')
        group.course_code = course[0]
        group.section = course[1]
        group.status = 'IDLE'
        group.instructor = cleaned_data['instructor']
        group.save()
        group.members.add(request.user)
        for member in cleaned_data['members']:
            group.members.add(member)
        messages.success(request, "Group has been SUCCESSFULLY added, thank you!")
        return redirect('learners:dashboard')
    return render(request, 'learners/add_group.html', {'group_form': group_form})


@login_required(login_url='users:login')
@learner_required
def process_submission(request, group_id):
    try:
        group = request.user.group_set.get(id=group_id)
    except Group.DoesNotExist:
        return Http404('Requested Group does Not exist')
    if group.status == 'ACCEPTED':
        form = DocumentForm(initial={'group_id': group_id})
        return render(request, 'documents/demo_submission.html', {'form': form})
    elif group.status == 'REQUESTED':
        messages.info(
            request,
            "Your permission for paper submission request is Pending."
            "To submit your paper, please visit again after the request has been accepted."
        )
    else:
        group.status = 'REQUESTED'
        group.save()
        messages.info(
            request,
            "Request to Approve Submission had been sent to your Instructor."
            "To submit your paper, please visit again after the request has been accepted."
        )
    return redirect('learners:dashboard')
