from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator


# Create your models here.
class User(AbstractUser):
    username = models.CharField(
        error_messages={'unique': 'A user with that username already exists.'},
        help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.',
        max_length=150,
        unique=True,
        primary_key=True,
        validators=[UnicodeUsernameValidator()],
        verbose_name='username')
