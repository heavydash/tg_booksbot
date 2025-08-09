from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.book import Book
from typing import List

class BookRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self) -> List[Book]:
        result = await self.session.execute(select(Book))
        books = result.scalars().all()
        print(f"Books retrieved: {[book.title for book in books]}")
        return books

    async def add_book(self, book: Book) -> Book:
        self.session.add(book)
        await self.session.commit()
        await self.session.refresh(book)
        return book
