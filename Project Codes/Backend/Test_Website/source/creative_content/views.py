from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, Http404, HttpResponse
from .models import Content, Resource
from .methods import generate_link
from .forms import ResourceForm

# Create your views here.


def index(request):
    print(Resource.objects.all().delete())
    contents = Content.objects.all()
    print(contents)
    context = {'contents': contents}
    return render(request, 'creative_content/index.html', context)


def demo_editor(request):
    return render(request, 'pages/demo_editor.html')


@login_required(login_url='users:login')
def editor(request):
    form = ResourceForm()
    if request.method == 'POST':
        link = generate_link()
        user = 'User 1'
        course_id = request.POST['course_id'].split('.')
        content = Content(link=link, title=request.POST['title'], content=request.POST['content'], user_name=user,
                          course_code=course_id[0], section=course_id[1])
        content.save()
        url = f'/content/{link}/show'
        print(url)
        return redirect(url)
    return render(request, 'creative_content/editor.html', {'form': form})


def upload_file(request):
    form = ResourceForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        resource = form.save(commit=False)
        resource.user = request.user
        resource.save()
    return redirect('/')


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
