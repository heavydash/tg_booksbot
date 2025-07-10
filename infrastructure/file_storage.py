import os
from config import BOOKS_DIR

class FileStorage:
    @staticmethod
    def get_file_path(file_name: str) -> str:
        """Возвращает полный путь к файлу."""
        return os.path.join(BOOKS_DIR, file_name)

    @staticmethod
    def file_exists(file_name: str) -> bool:
        """Проверяет существование файла."""
        return os.path.exists(os.path.join(BOOKS_DIR, file_name))
