from django.shortcuts import render, redirect, Http404
from .models import Content
from .methods import generate_link
from django.core.files.storage import FileSystemStorage

# Create your views here.


def demo_editor(request):
    return render(request, 'pages/demo_editor.html')


def editor(request):
    if request.method == 'POST' and request.FILES['upload_file'] is not None:
        uploaded_file = request.FILES['upload_file']
        file_system = FileSystemStorage()
        file_name = file_system.save(uploaded_file.name, uploaded_file)
        url = f'/static/{file_system.url(file_name)}'
        print(url)
    elif request.method == 'POST':
        link = generate_link()
        user = 'User 1'
        course_id = request.POST['course_id'].split('.')
        content = Content(link=link, title=request.POST['title'], content=request.POST['content'], user_name=user,
                          course_code=course_id[0], section=course_id[1])
        content.save()
        url = f'/content/{link}/show'
        print(url)
        return redirect(url)
    return render(request, 'creative_content/editor.html')


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
