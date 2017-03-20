from random import choice

SLUG_ALLOWED_CHARACTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'


def generate_random_slug(length=6):
    return ''.join([choice(SLUG_ALLOWED_CHARACTERS) for _ in range(length)])
