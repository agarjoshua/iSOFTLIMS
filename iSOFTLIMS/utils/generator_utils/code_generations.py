from django.db import models
import random

def generate_custom_code(model_fields):
    code = ""

    for i, field in enumerate(model_fields[:3]):
        
        code+=f'{_get_first_letters_forward(field)}-'
        # code += f"{field_name}-{unique_number} = models.{field_type}(max_length=255)\n"
    unique_number = str(random.randint(0, 1000)).zfill(4)
    code += f'{unique_number}'
    print(code)
    return code

def _get_first_letters_forward(string):
    words = string.split()
    first_letters = [word[0] for word in words]
    return ''.join(first_letters)