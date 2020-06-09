import random


def create_new_ref_number():
    return str(random.sample(range(999999), 1))
