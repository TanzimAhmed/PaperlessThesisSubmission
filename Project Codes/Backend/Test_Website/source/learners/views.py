from django.shortcuts import render, redirect, Http404
from .forms import CreateGroupForm, GroupSelectForm
from .models import Group


# Create your views here.
def dashboard(request):
    print(Group.objects.all())
    groups_form = GroupSelectForm(request.POST or None)
    groups_form.update_choice(request.user)
    if groups_form.is_valid():
        return render(request, 'learners/request_submission.html', {'groups_form': groups_form})
    return render(request, 'learners/dashboard.html', {'groups_form': groups_form})


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
        print(group.members.all())
    return render(request, 'learners/_dashboard.html', {'group_form': group_form})


def request_submission(request):
    groups_form = GroupSelectForm(request.POST)
    groups_form.update_choice(request.user)
    if groups_form.is_valid():
        try:
            group = Group.objects.get(id=groups_form.cleaned_data['groups'])
        except Group.DoesNotExist:
            raise Http404('Group Not Found')
        else:
            group.status = 'REQUESTED'
    return redirect('documents:upload_paper')