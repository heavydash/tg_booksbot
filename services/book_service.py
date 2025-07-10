from repositories.book_repository import BookRepository
from infrastructure.file_storage import FileStorage
from models.book import Book
from typing import List

class BookService:
    def __init__(self, book_repository: BookRepository, file_storage: FileStorage):
        self.book_repository = book_repository
        self.file_storage = file_storage

    async def get_all_books(self) -> List[Book]:
        return await self.book_repository.get_all_books()
