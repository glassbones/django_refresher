import uuid

def get_random_eight_digit_id():
    code = str(uuid.uuid4())[:8].replace('-', '').lower()
    return code