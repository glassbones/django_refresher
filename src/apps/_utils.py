import uuid

def get_random_eight_digit_id():
    code = str(uuid.uuid4())[:8].replace('-', '').lower()
    return code

def if_less_than_one_return_zero(value):
    if value > 1: return 0
    else: return value