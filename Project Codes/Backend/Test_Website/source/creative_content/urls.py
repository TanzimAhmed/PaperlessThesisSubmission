from django.urls import path
from .views import index, show, EditView, DeleteView, DeleteResourceView, upload_file, editor

app_name = 'creative_contents'
urlpatterns = [
    path('', index, name='index'),
    path('<str:link>/show/', show, name='display'),
    path('<str:link>/edit/', EditView.as_view(), name='edit'),
    path('editor/', editor, name='editor'),
    path('upload/', upload_file, name='upload_file'),
    path('delete/', DeleteView.as_view(), name='delete'),
    path('asset/delete/', DeleteResourceView.as_view(), name='resource_delete')
]
