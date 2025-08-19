from dataclasses import dataclass
from models.book import Book
from typing import List
from repositories.book_repository import BookRepository
from infrastructure.file_storage import FileStorage

@dataclass
class Book:
    title: str
    author: str
    format: str

class BookService:
    def __init__(self, book_repository: BookRepository, file_storage: FileStorage):
        self.book_repository = book_repository
        self.file_storage = file_storage

    async def get_all_books(self) -> List[Book]:
        return await self.book_repository.get_all()

    async def search_books(query:str) -> List[Book]:
        query = query.lower()
        books = await self.book_repository.get_all()
        print(f"Books in search_books: {[book.title for book in books]}")
        filtered_books = [
            book for book in books
            if (book.title and query in book.title.lower()) or (book.author and
            query in book.author.lower())
        ]
        print(f"Filtered books: {[book.title for book in filtered_books]}")
        print(f"Returning filtered_books with {len(filtered_books)} items")
        return filtered_books

    async def add_book(self, title: str, author: str, format: str, file_id: str, file_name: str) -> Book:
        book = Book(title=title, author=author, format=format, file_id=file_id)
        return await self.book_repository.add_book(book)





