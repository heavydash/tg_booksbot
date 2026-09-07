import logging
from aiogram import Dispatcher, types
from aiogram.filters import Command
from services.book_service import BookService
from infrastructure.database import get_session
from repositories.book_repository import BookRepository
from infrastructure.file_storage import FileStorage

logger = logging.getLogger(__name__)
async def send_welcome(message: types.Message):
    logger.info(f"Received /start from {message.from_user.id}")
    await message.reply("Welcome to the Book Bot!\n/list - List all books\n/help - Help")


async def send_help(message: types.Message):
    logger.info(f"Received /help from {message.from_user.id}")
    await message.reply("Commands:\n/list - List all books")


async def list_books(message: types.Message):
    logger.info(f"Received /list from {message.from_user.id}")
    async for session in get_session():
        book_service = BookService(BookRepository(session), FileStorage())
        books = await book_service.get_all_books()
        if not books:
            await message.reply("No books available")
            return
        response = "\n".join(
            [f"{book.title} by {book.author} ({book.format.upper()})" for book in books]
        )
        await message.reply(f"Books:\n{response}")


def register_handlers(dp: Dispatcher):
    logger.info("Registering handlers")
    dp.message.register(send_welcome, Command("start"))
    dp.message.register(send_help, Command("help"))
    dp.message.register(list_books, Command("list"))