# embroidery_designs/designs/validators.py

import os
from django.core.exceptions import ValidationError

def validate_embroidery_file(value):
    """
    Валидатор для файлов вышивальных машин
    Работает с оригинальными расширениями включая jef+
    """
    if not value:
        return
    
    ext = os.path.splitext(value.name)[1].lower()
    
    valid_extensions = [
        '.pes', '.dst', '.jef', '.exp', 
        '.jef+',  # ← ОРИГИНАЛЬНОЕ расширение
        '.vp3', '.xxx', '.hus', '.vip', '.pcs', '.pcq', '.sew'
    ]
    
    if ext not in valid_extensions:
        raise ValidationError(
            f'Неподдерживаемый формат файла: {ext}. '
            f'Поддерживаемые форматы: PES, DST, JEF, EXP, JEF+, VP3, XXX и др.'
        )