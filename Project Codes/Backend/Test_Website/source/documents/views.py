from django.shortcuts import render
from .forms import DocumentForm
from .models import Document
from .pages import PdfDocumentTest

# Create your views here.


def upload_paper(request):
    form = DocumentForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        document = form.save(commit=False)
        document.username = request.user
        document.instructor_id = request.user
        document.status = 'UPLOADED'
        document.information = 'None'
        document.save()
        document_test = PdfDocumentTest(document.paper.path)
        if document_test.is_valid_format():
            document.status = 'PENDING'
            document.save()
            message = "Your Paper is successfully submitted to the instructor. Please wait for instructor's approval" \
                      "and visit again later."
            return render(request, 'documents/log.html', {'message': message})
        else:
            context = {
                'message': "Your paper contains errors",
                'errors': document_test.errors
            }
            document.delete()
            return render(request, 'documents/log.html', context)
    print('Documents', Document.objects.all())
    return render(request, 'documents/demo_submission.html', {'form': form})
