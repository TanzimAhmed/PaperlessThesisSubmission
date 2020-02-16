from django.db import models

# Create your models here.


class Content(models.Model):
    content = models.TextField()
    link = models.CharField(max_length=50, primary_key=True)
    title = models.CharField(max_length=200)
    user_name = models.CharField(max_length=100)
    course_code = models.CharField(max_length=15)
    section = models.IntegerField()

    def __str__(self):
        return self.link
