import random
import string


def generate_password(length=18):
    """
    Generate a strong, unique password of a given length.

    The password will contain:
    - Uppercase Letters (A-Z)
    - Lowercase Letters (a-z)
    - Digits (0-9)
    - Special Characters (!@#$%^&*()_+)

    :param length: Length of the password (default: 14)
    :return: Randomly generated secure password
    """
    if length < 8:
        raise ValueError("Password length must be at least 8 characters for security.")

    characters = (
        string.ascii_uppercase + string.ascii_lowercase + string.digits + "!@#$%^&*()_+"
    )

    password = "".join(random.choice(characters) for _ in range(length))

    return password
