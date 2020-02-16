import random
import string
from .models import Content


def generate_link():
    """Random String Generator"""
    temp_link = random_string(8)
    try:
        Content.objects.get(link=temp_link)
    except Content.DoesNotExist:
        return temp_link
    else:
        return generate_link()


def random_string(self, string_length=6):
    """Generate a random string of letters and digits """
    letters_and_digits = string.ascii_letters + string.digits
    return ''.join(random.choice(letters_and_digits) for i in range(string_length))
