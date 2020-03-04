from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.validators import MinLengthValidator


# Create your models here.
class User(AbstractUser):
    username = models.CharField(
        error_messages={'unique': 'A user with that username already exists.'},
        help_text='Required. 10 characters or fewer.',
        max_length=10,
        unique=True,
        primary_key=True,
        validators=[UnicodeUsernameValidator(), MinLengthValidator(3)],
        verbose_name='username')


class Group(models.Model):
    course_code = models.CharField(max_length=30)
    section = models.IntegerField()
    name = models.CharField(max_length=128)
    upload = models.BooleanField()
    members = models.ManyToManyField(User)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['course_code', 'section', 'name'], name='unique_group')
        ]

    def get_string(self):
        return f'Group: {self.name}, Course: {self.course_code}, Section: {self.section}'

    def __str__(self):
        return f'{self.course_code}.{self.section}_{self.name}'
