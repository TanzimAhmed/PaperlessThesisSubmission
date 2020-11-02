from django.contrib import messages
from django.shortcuts import render, redirect, Http404, get_object_or_404
from django.http import FileResponse
from django.core.exceptions import PermissionDenied
from django.views import View
from django.utils.decorators import method_decorator
from .models import Document
from .forms import DocumentForm, DocumentVerificationForm
from .pages import PdfDocumentTest
from learners.models import Group
from project_paperless.utils import login_required, learner_required, educator_required


# Create your views here.
@login_required(login_url='users:login')
@learner_required
def upload_paper(request):
    form = DocumentForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        try:
            group = request.user.group_set.get(id=form.cleaned_data['group_id'])
        except Group.DoesNotExist:
            raise Http404('Group Not found')
        if group.status != 'ACCEPTED':
            raise PermissionDenied
        print('uploading paper')
        document = form.save(commit=False)
        document.group = group
        document.information = ''
        document.save()
        document_test = PdfDocumentTest(document.paper.path)
        if document_test.is_valid_format():
            messages.success(request, "Your Paper is SUCCESSFULLY uploaded, thank you!")
            return redirect('users:dashboard')
        else:
            messages.warning(request, "Your paper contains errors")
            document.delete()
            return render(request, 'documents/log.html', {'errors': document_test.errors})
    return render(request, 'documents/submission.html', {'form': form})


class ShowView(View):
    def get(self, request):
        raise Http404('URL Not found')

    @method_decorator(login_required(login_url='users:login'))
    def post(self, request):
        if 'document_id' and 'group_id' in request.POST:
            document_id = request.POST['document_id']
            group_id = request.POST['group_id']
        else:
            raise PermissionDenied('Unauthorized')

        try:
            if request.user.is_educator:
                group = request.user.submission_group.get(id=group_id)
            else:
                group = request.user.group_set.get(id=group_id)
            document = group.document.get(id=document_id)
        except (Group.DoesNotExist, Document.DoesNotExist):
            raise PermissionDenied('Matching group and document Not found')

        file = open(document.paper.path, 'rb')
        return FileResponse(file, filename=document.paper.name, as_attachment=False)


def check_document(request):
    form = DocumentVerificationForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        document_id = form.cleaned_data['document_id']
        uploaded_document = request.FILES['document']
        document = get_object_or_404(Document, id=document_id)
        if document.verify(uploaded_document):
            messages.success(request, 'This is the actual copy of the file.')
        else:
            messages.warning(request, 'This file is has been Modified or Manipulated Illegally.')
        form = DocumentVerificationForm()
    return render(request, 'documents/verification.html', {'form': form})
