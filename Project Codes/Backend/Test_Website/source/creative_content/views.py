from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, Http404, HttpResponse
from django.core.exceptions import PermissionDenied
from .models import Content, Resource
from .methods import generate_link
from .forms import ContentForm, ResourceForm

# Create your views here.


def index(request):
    print(Resource.objects.all())
    contents = Content.objects.all()
    context = {'contents': contents}
    return render(request, 'creative_content/index.html', context)


def demo_editor(request):
    return render(request, 'pages/demo_editor.html')


@login_required(login_url='users:login')
def editor(request):
    content_form = ContentForm(request.POST or None)
    resource_form = ResourceForm()
    resources = request.user.resource_set.all()

    if content_form.is_valid():
        link = generate_link()
        content = content_form.save(commit=False)
        content.user = request.user
        content.link = link
        course = content_form.cleaned_data['course'].split('.')
        content.course_code = course[0]
        content.section = course[1]
        content.save()
        url = f'/content/{link}/show/'
        return redirect(url)

    context = {
        'content_form': content_form,
        'resource_form': resource_form,
        'resources': resources
    }
    return render(request, 'creative_content/editor.html', context)


@login_required(login_url='users:login')
def edit(request, link):
    try:
        content = Content.objects.get(link=link)
    except Content.DoesNotExist:
        raise Http404('Link does not exist')

    if content.user != request.user:
        raise PermissionDenied

    data = {
        'content': content.content,
        'title': content.title,
        'course': f'{content.course_code}.{content.section}'
    }
    content_form = ContentForm(data)
    resource_form = ResourceForm()
    resources = request.user.resource_set.all()

    if request.method == 'POST':
        content_form = ContentForm(request.POST)
        if content_form.is_valid():
            edited_data = content_form.cleaned_data
            content.content = edited_data['content']
            content.title = edited_data['title']
            course = edited_data['course'].split('.')
            content.course_code = course[0]
            content.section = course[1]
            content.save()
            url = f'/content/{link}/show/'
            return redirect(url)

    context = {
        'edit': True,
        'content_form': content_form,
        'resource_form': resource_form,
        'resources': resources,
        'content': content
    }
    return render(request, 'creative_content/editor.html', context)


def upload_file(request):
    form = ResourceForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        resource = form.save(commit=False)
        resource.user = request.user
        resource.save()
        return HttpResponse(resource.item.url)
    else:
        return HttpResponse('Resource not valid, please upload again')


def show(request, link):
    try:
        content = Content.objects.get(link=link)
    except Content.DoesNotExist:
        raise Http404('Link does not exist')
    else:
        context = {'content': content}
        return render(request, 'creative_content/content_display.html', context)


def content_display(request):
    return render(request, 'creative_content/content_display.html')
