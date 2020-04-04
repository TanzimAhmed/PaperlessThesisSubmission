from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, Http404, HttpResponse
from django.http import JsonResponse
from django.core.exceptions import PermissionDenied
from django.views import View
from django.utils.decorators import method_decorator
from .models import Content, Resource
from project_paperless.utils import unique_id
from .forms import ContentForm, DiscussionForm, RepliesForm, ResourceForm

# Create your views here.


def index(request):
    print(Resource.objects.all())
    contents = Content.objects.all()
    context = {'contents': contents}
    return render(request, 'creative_content/index.html', context)


@login_required(login_url='users:login')
def editor(request):
    content_form = ContentForm(request.POST or None)
    resource_form = ResourceForm()
    resources = request.user.resource.all()

    if content_form.is_valid():
        link = unique_id(model=Content, target_column='link')
        content = content_form.save(commit=False)
        content.user = request.user
        content.link = link
        course = content_form.cleaned_data['course'].split('.')
        content.course_code = course[0]
        content.section = course[1]
        content.save()
        return redirect('creative_contents:display', link)

    context = {
        'content_form': content_form,
        'resource_form': resource_form,
        'resources': resources
    }
    print(context)
    return render(request, 'creative_content/editor.html', context)


class EditView(View):
    template_name = 'creative_content/editor.html'
    content = None
    request = None

    @method_decorator(login_required(login_url='users:login'))
    def get(self, request, link):
        self.request = request
        content = self.get_content(link)

        data = {
            'content': content.content,
            'title': content.title,
            'course': f'{content.course_code}.{content.section}'
        }

        content_form = ContentForm(data)
        return render(request, self.template_name, self.context(content_form))

    @method_decorator(login_required(login_url='users:login'))
    def post(self, request, link):
        self.request = request
        content = self.get_content(link)

        content_form = ContentForm(request.POST)
        if content_form.is_valid():
            edited_data = content_form.cleaned_data
            content.content = edited_data['content']
            content.title = edited_data['title']
            course = edited_data['course'].split('.')
            content.course_code = course[0]
            content.section = course[1]
            content.save()
            return redirect('creative_contents:edit', link)
        return render(request, self.template_name, self.context(content_form))

    def context(self, content_form):
        resource_form = ResourceForm()
        resources = self.request.user.resource.all()

        context = {
            'content_form': content_form,
            'resource_form': resource_form,
            'resources': resources,
            'content': self.content
        }
        return context

    def get_content(self, link):
        try:
            self.content = self.request.user.content.get(link=link)
        except Content.DoesNotExist:
            raise Http404('Link does not exist')
        return self.content


class DeleteResourceView(View):
    def get(self, request):
        raise Http404('Url does not exist')

    def post(self, request):
        print(request.POST)
        if 'resource_id' in request.POST:
            resource_id = request.POST['resource_id']
        else:
            raise HttpResponse('No image File', status=400)
        try:
            resource = request.user.resource.get(id=resource_id)
        except Content.DoesNotExist:
            raise HttpResponse('Resource does NOT exist', status=403)
        resource.delete()
        return HttpResponse('Resource Deleted')


def upload_file(request):
    form = ResourceForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        resource = form.save(commit=False)
        resource.user = request.user
        resource.save()
        data = {
            'id': resource.id,
            'url': resource.item.url
        }
        return JsonResponse(data)
    else:
        return HttpResponse('Invalid Image', status=400)


def show(request, link):
    try:
        content = Content.objects.get(link=link)
    except Content.DoesNotExist:
        raise Http404('Link does not exist')

    discussions = content.discussion.all()
    discussion_form = DiscussionForm()
    replies_form = RepliesForm()
    context = {
        'content': content,
        'discussions': discussions,
        'discussion_form': discussion_form,
        'replies_form': replies_form
    }
    print(context)
    return render(request, 'creative_content/content_display.html', context)


def content_display(request):
    return render(request, 'creative_content/content_display.html')
