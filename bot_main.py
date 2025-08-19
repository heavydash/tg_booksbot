import asyncio
from aiogram import Bot, Dispatcher
from handlers.middleware import BookServiceMiddleware
from handlers.start import router as start_router
from handlers.search import router as search_router
from handlers.add_book import router as add_book_router
from handlers.admin import router as admin_router
from infrastructure.database import get_session
from repositories.book_repository import BookRepository
from infrastructure.file_storage import FileStorage
from services.book_service import BookService

async def main():
    bot = Bot(token="6718966474:AAFvgVErUf4IHuFFN5wePb5AsH11A5262ms")
    dp = Dispatcher()
    async for session in get_session():
        book_service = BookService(BookRepository(session), FileStorage())
        dp.message.middleware(BookServiceMiddleware(book_service))
        dp.include_router(start_router)
        dp.include_router(search_router)
        dp.include_router(add_book_router)
        dp.include_router(admin_router)
        await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
