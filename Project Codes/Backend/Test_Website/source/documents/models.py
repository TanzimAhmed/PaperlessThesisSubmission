from django.core.files.storage import FileSystemStorage
from django.db import models
from os.path import join as join_dir
from django.conf import settings


# Create your models here.
paper_storage = FileSystemStorage(location=join_dir(settings.BASE_DIR, 'storage/'))


def user_directory_path(instance, file_name):
    return f'{instance.group}/{file_name}'


class Document(models.Model):
    group = models.ForeignKey('learners.Group', on_delete=models.CASCADE)
    instructor = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='instructor')
    paper = models.FileField(storage=paper_storage, upload_to=user_directory_path)
    information = models.CharField(max_length=250)
    status = models.CharField(max_length=10)

    def delete(self, using=None, keep_parents=False):
        self.paper.storage.delete(self.paper.name)
        super().delete(using=using, keep_parents=keep_parents)

    def accept(self):
        self.status = 'ACCEPTED'
        self.information = f'Your Paper: {self.paper.name} is ACCEPTED by {self.instructor_id}'

    def reject(self, message=None):
        self.status = 'REJECTED'
        self.information = f'Your Paper: {self.paper.name} is REJECTED by {self.instructor_id}' + message

    def __str__(self):
        return f'Paper: {self.paper.name}, submitted by: {self.group}, to {self.instructor_id}'
