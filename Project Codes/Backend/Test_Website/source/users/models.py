from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.validators import MinLengthValidator
from django.utils.timezone import now as current_time, timedelta


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
    is_educator = models.BooleanField(default=False)


class Verification(models.Model):
    username = models.CharField(primary_key=True, max_length=10)
    token = models.CharField(max_length=10)
    is_verified = models.BooleanField(default=False)
    time_stamp = models.DateTimeField(auto_now=True)

    @classmethod
    def add_token(cls, username, token):
        try:
            verification = Verification.objects.get(username=username)
        except Verification.DoesNotExist:
            verification = Verification(username=username, token=token)
            verification.save()
            return verification
        else:
            verification.token = token
            verification.save()
            return verification

    def time_check(self):
        return (self.time_stamp + timedelta(minutes=5)) >= current_time()
