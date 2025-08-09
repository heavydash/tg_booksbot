import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from infrastructure.database import get_session
from repositories.book_repository import BookRepository
from models.book import Book

async def add_sample_books():
    async for session in get_session():
        repo = BookRepository(session)
        books = [
            Book(title="War and Peace", author="Leo Tolstoy", format="pdf", file_path="war_and_peace.pdf"),
            Book(title="1984", author="George Orwell", format="epub", file_path="1984.epub")
        ]
        for book in books:
            await repo.add_book(book)

if __name__ == '__main__':
    asyncio.run(add_sample_books())
