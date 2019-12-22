from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    allowed_range = range(1, 6)
    context = {'allowed_range': allowed_range}
    return render(request, 'pages/cover_page.html', context=context)
