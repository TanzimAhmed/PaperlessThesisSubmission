from django.shortcuts import render

# Create your views here.


def demo_editor(request):
    return render(request, 'pages/demo_editor.html')
