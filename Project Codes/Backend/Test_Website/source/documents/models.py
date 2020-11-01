from django.core.files.storage import FileSystemStorage
from django.db import models
from os.path import join as join_dir
from django.conf import settings
from hashlib import sha3_512


# Create your models here.
paper_storage = FileSystemStorage(location=join_dir(settings.BASE_DIR, 'storage/'))


def user_directory_path(instance, file_name):
    return f'{instance.group}/{file_name}'


class Document(models.Model):
    group = models.ForeignKey('learners.Group', on_delete=models.CASCADE, related_name='document')
    title = models.CharField(max_length=250)
    paper = models.FileField(storage=paper_storage, upload_to=user_directory_path)
    information = models.CharField(max_length=250, null=True)
    date_uploaded = models.DateTimeField(auto_now_add=True, editable=False)
    date_updated = models.DateTimeField(auto_now=True)

    def delete(self, using=None, keep_parents=False):
        self.paper.storage.delete(self.paper.name)
        super().delete(using=using, keep_parents=keep_parents)

    def get_string(self):
        return f'{self.group}_{self.paper.name}'

    def verify(self, uploaded_file):
        with open(self.paper.path, 'rb') as source_file:
            source_hash = sha3_512(source_file.read())
            uploaded_hash = sha3_512(uploaded_file.read())
            if source_hash.hexdigest() == uploaded_hash.hexdigest():
                return True
            else:
                return False

    def __str__(self):
        return f'Paper: {self.paper.name}, submitted by: {self.group}, to {self.group.instructor}'
