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

    async def search_books(self, query: str) -> List[Book]:
        query = query.lower()
        books = await self.book_repository.get_all()
        print(f"Books in search_books: {[book.title for book in books]}")
        filtered_books = [
            book for book in books
            if (book.title and query in book.title.lower()) or (book.author and query in book.author.lower())
        ]
        print(f"Filtered books: {[book.title for book in filtered_books]}")
        print(f"Returning filtered_books with {len(filtered_books)} items")  # Дополнительная отладка
        return filtered_books