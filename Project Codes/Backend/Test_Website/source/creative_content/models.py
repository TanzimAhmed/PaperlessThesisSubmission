from django.db import models


# Create your models here.
def user_directory_path(instance, file_name):
    return f'uploads/{instance.user}/{file_name}'


class Content(models.Model):
    content = models.TextField()
    link = models.CharField(max_length=50, primary_key=True)
    title = models.CharField(max_length=200)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    course_code = models.CharField(max_length=15)
    section = models.IntegerField()
    date_created = models.DateTimeField(auto_now_add=True, editable=False)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.link


class Resource(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    item = models.FileField(upload_to=user_directory_path)

    def delete(self, using=None, keep_parents=False):
        self.item.storage.delete(self.item.name)
        super().delete(using=using, keep_parents=keep_parents)

    def __str__(self):
        return self.item.name


class DiscussionThread(models.Model):
    pass
