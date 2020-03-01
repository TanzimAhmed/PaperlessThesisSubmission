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
        validators=[UnicodeUsernameValidator(), MinLengthValidator(8)],
        verbose_name='username')
