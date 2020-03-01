from django.shortcuts import render
from .forms import DocumentForm
from .models import Document

# Create your views here.


def upload_paper(request):
    form = DocumentForm(request.POST or None, request.FILES or None)
    print(request.FILES)
    if form.is_valid():
        document = form.save(commit=False)
        document.username = request.user
        document.instructor_id = request.user
        document.status = 'UPLOADED'
        document.information = 'None'
        document.save()
        form = DocumentForm()
    print('Documents', Document.objects.all())
    return render(request, 'pages/demo_submission.html', {'form': form})
