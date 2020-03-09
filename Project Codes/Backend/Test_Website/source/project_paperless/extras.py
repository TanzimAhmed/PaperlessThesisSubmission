import random
import string
from django.utils.timezone import datetime


COURSE_CHOICE_LIST = [
    ('CSE 499A.21', 'CSE 499A, Section 21'),
    ('CSE 499B.15', 'CSE 499B, Section 15'),
]

year = datetime.now().year

SEMESTER_CHOICE_LIST = [
    (f'SP_{year}', f'Spring {year}'),
    (f'SM_{year}', f'Summer {year}'),
    (f'FL_{year}', f'Fall {year}'),
]


def unique_id(model, target_column='id', length=8):
    """Random String Generator"""
    temp_link = random_string(length)
    try:
        model.objects.get(**{target_column: temp_link})
    except model.DoesNotExist:
        return temp_link
    else:
        return unique_id(model=model, target_column=target_column)


def random_string(string_length):
    """Generate a random string of letters and digits """
    letters_and_digits = string.ascii_letters + string.digits
    return ''.join(random.choice(letters_and_digits) for i in range(string_length))
