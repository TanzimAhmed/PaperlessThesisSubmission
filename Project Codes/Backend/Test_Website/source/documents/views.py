from django.contrib import messages
from django.shortcuts import render
from .forms import DocumentForm
from .models import Document
from .pages import PdfDocumentTest

# Create your views here.


def upload_paper(request):
    form = DocumentForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        document = form.save(commit=False)
        document.user = request.user
        document.instructor = request.user
        document.status = 'UPLOADED'
        document.information = 'None'
        document.save()
        document_test = PdfDocumentTest(document.paper.path)
        if document_test.is_valid_format():
            document.status = 'PENDING'
            document.save()
            messages.success(
                request,
                "Your Paper is successfully submitted to the instructor. Please wait for instructor's approval "
                "and visit your dashboard again, later."
            )
            return render(request, 'documents/log.html')
        else:
            messages.warning(request, "Your paper contains errors")
            document.delete()
            return render(request, 'documents/log.html', {'errors': document_test.errors})
    print('Documents', Document.objects.all())
    return render(request, 'documents/demo_submission.html', {'form': form})
