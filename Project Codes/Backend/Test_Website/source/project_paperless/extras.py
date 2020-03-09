import random
import string


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
