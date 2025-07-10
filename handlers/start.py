from aiogram import Dispatcher, types
from services.book_service import BookService
from infrastructure.database import get_session
from repositories.book_repository import BookRepository
from infrastructure.file_storage import FileStorage

def register_handlers(dp: Dispatcher):
    print("Registering handlers")
    @dp.message_handler(commands=['start'])
    async def send_welcome(message: types.Message):
        print(f"Received /start from {message.from_user.id}")  # Для отладки
        await message.reply("Welcome to the Book Bot!\n/list - List all books\n/help - Help")

    @dp.message_handler(commands=['help'])
    async def send_help(message: types.Message):
        print(f"Received /help from {message.from_user.id}")  # Для отладки
        await message.reply("Commands:\n/list - List all books")

    @dp.message_handler(commands=['list'])
    async def list_books(message: types.Message):
        print(f"Received /list from {message.from_user.id}")  # Для отладки
        async for session in get_session():
            book_service = BookService(BookRepository(session), FileStorage())
            books = await book_service.get_all_books()
            if not books:
                await message.reply("No books available.")
                return
            response = "\n".join(
                [f"{book.title} by {book.author} ({book.format.upper()})" for book in books]
            )
            await message.reply(f"Books:\n{response}")
