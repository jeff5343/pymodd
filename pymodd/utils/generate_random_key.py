import random
import string


def generate_random_key() -> str:
    return "".join(random.choices(string.ascii_letters + string.digits, k=10))
