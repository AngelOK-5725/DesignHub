# embroidery_designs/embroidery_designs/storage.py
from django.core.files.storage import FileSystemStorage
from django.utils.text import get_valid_filename

class PlusFriendlyStorage(FileSystemStorage):
    def get_valid_name(self, name):
        """
        Разрешаем '+' в именах файлов
        """
        # Оригинальный метод Django удаляет '+'
        # поэтому реализуем упрощённый вариант
        name = name.strip().replace(' ', '_')
        return name  # оставляем '+' как есть
