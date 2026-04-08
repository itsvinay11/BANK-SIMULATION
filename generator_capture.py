import string
import random

def random_capture(length=4):
    chars=string.ascii_uppercase+string.digits+string.ascii_lowercase
    capture=" ".join(random.choice(chars) for _ in range(length))
    return capture

def random_password(length=6):
    chars=string.ascii_uppercase+string.digits+string.ascii_lowercase
    password="".join(random.choice(chars) for _ in range(length))
    return password


def close_otp(length=4):
    otp=random.randint(1000,9999)
    return otp


def forgot_otp(length=4):
    otp=random.randint(1000,9999)
    return otp
