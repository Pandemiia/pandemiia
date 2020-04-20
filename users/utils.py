import re
import uuid


def generate_random_username(salt_length=8, random_value_length=30, **kwargs):
    first_name = kwargs.get('first_name', '')
    last_name = kwargs.get('last_name', '')
    email = kwargs.get('email', '')

    if first_name or last_name:
        template = f'{first_name}{last_name}'.strip()
    elif email:
        template = re.sub(r'\W+', '', email.split('@')[0])
    else:
        template = uuid.uuid4().hex[:random_value_length]

    username = template + uuid.uuid4().hex[:salt_length]

    return username.lower()
