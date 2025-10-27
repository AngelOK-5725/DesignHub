# embroidery_designs/designs/patches.py

"""
Патч для Django чтобы принимать расширения с символами + в именах файлов
"""
import os
import django.core.validators
import django.utils.deconstruct
from django.core.exceptions import ValidationError

# Сохраняем оригинальный валидатор
_original_file_validator = django.core.validators.FileExtensionValidator

@django.utils.deconstruct.deconstructible
class PatchedFileExtensionValidator(_original_file_validator):
    def __call__(self, value):
        """
        Переопределяем валидацию файлов чтобы принимать расширения с +
        """
        if not hasattr(value, 'name'):
            return
        
        # Проходим базовую валидацию
        try:
            super().__call__(value)
        except ValidationError:
            # Если базовая валидация не прошла, проверяем расширения с +
            extension = os.path.splitext(value.name)[1][1:].lower()
            if extension not in self.allowed_extensions:
                raise ValidationError(
                    self.message,
                    code=self.code,
                    params={
                        'extension': extension,
                        'allowed_extensions': ', '.join(self.allowed_extensions)
                    }
                )

# Применяем патч
django.core.validators.FileExtensionValidator = PatchedFileExtensionValidator