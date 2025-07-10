from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.book import Book
from typing import List

class BookRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all_books(self) -> List[Book]:
        result = await self.session.execute(select(Book))
        return result.scalars().all()

    async def add_book(self, book: Book) -> Book:
        self.session.add(book)
        await self.session.commit()
        await self.session.refresh(book)
        return book
