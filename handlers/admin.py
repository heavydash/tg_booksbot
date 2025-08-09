# handlers/admin.py
from aiogram import Dispatcher, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from services.book_service import BookService
from infrastructure.database import get_session
from repositories.book_repository import BookRepository
from infrastructure.file_storage import FileStorage
from config import ADMIN_IDS

class AddBookForm(StatesGroup):
    title = State()
    author = State()
    format = State()
    file = State()

def register_handlers(dp: Dispatcher):
    @dp.message(Command(commands=['add_book']), lambda message: message.from_user.id in ADMIN_IDS)
    async def start_add_book(message: types.Message, state: FSMContext):
        await state.set_state(AddBookForm.title)
        await message.reply("Enter book title:")

    @dp.message(AddBookForm.title)
    async def process_title(message: types.Message, state: FSMContext):
        await state.update_data(title=message.text)
        await state.set_state(AddBookForm.author)
        await message.reply("Enter author:")

    @dp.message(AddBookForm.author)
    async def process_author(message: types.Message, state: FSMContext):
        await state.update_data(author=message.text)
        await state.set_state(AddBookForm.format)
        await message.reply("Enter format (pdf, epub, mobi):")

    @dp.message(AddBookForm.format)
    async def process_format(message: types.Message, state: FSMContext):
        if message.text.lower() not in ['pdf', 'epub', 'mobi']:
            await message.reply("Format must be pdf, epub, or mobi!")
            return
        await state.update_data(format=message.text.lower())
        await state.set_state(AddBookForm.file)
        await message.reply("Send the book file:")

    @dp.message(AddBookForm.file, content_types=types.ContentType.DOCUMENT)
    async def process_file(message: types.Message, state: FSMContext, bot: types.Bot):
        document = message.document
        if document.file_size > 50 * 1024 * 1024:  # 50 MB
            await message.reply("File too large! Max 50 MB.")
            await state.clear()
            return
        data = await state.get_data()
        file = await bot.download(document.file_id)
        async for session in get_session():
            book_service = BookService(BookRepository(session), FileStorage())
            try:
                await book_service.add_book(
                    title=data['title'],
                    author=data['author'],
                    format=data['format'],
                    file_data=file.read(),
                    file_name=document.file_name
                )
                await message.reply("Book added successfully!")
            except ValueError as e:
                await message.reply(f"Error: {e}")
        await state.clear()