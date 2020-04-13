from django.contrib import messages
from django.shortcuts import render, redirect, Http404
from django.http import FileResponse
from django.core.exceptions import PermissionDenied
from django.views import View
from .forms import DocumentForm
from .pages import PdfDocumentTest
from learners.models import Group


# Create your views here.
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

    def post(self, request):
        if 'document_id' and 'group_id' in request.POST:
            document_id = request.POST['document_id']
            group_id = request.POST['group_id']
        else:
            raise PermissionDenied('Unauthorized')

        document = request.user.group_set.first().document.first()
        print(document.paper.path)
        file = open(document.paper.path, 'rb')
        return FileResponse(file, filename=document.paper.name, as_attachment=False)
