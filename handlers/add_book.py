from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup, default_state
from utils.keyboards import get_main_keyboard, get_cancel_keyboard
from aiogram.types import ContentType

router = Router()

class AddBookForm(StatesGroup):
    title = State()
    author = State()
    format = State()
    file = State()

@router.message(Command("add_book"))
@router.message(F.text=="Загрузить книгу", default_state)
async def start_add_book(message: types.Message, state: FSMContext) -> None:
    await state.set_state(AddBookForm.title)
    await message.reply("Введите название книги:",
    reply_markup=get_cancel_keyboard())


@router.message(AddBookForm.title)
async def process_title(message: types.Message, state: FSMContext) -> None:
    if message.text == "Отмена":
        await state.clear()
        await message.reply("Добавление книги отменено.",
        reply_markup=get_main_keyboard())
        return
    await state.update_data(title=message.text)
    await state.set_state(AddBookForm.author)
    await message.reply("Введите автора книги:",
    reply_markup=get_cancel_keyboard())


@router.message(AddBookForm.author)
async def process_author(message: types.Message, state: FSMContext) -> None:
    if message.text == "Отмена":
        await state.clear()
        await message.reply("Добавление книги отменено.",
        reply_markup=get_main_keyboard())
        return
    await state.update_data(author=message.text)
    await state.set_state(AddBookForm.format)
    await message.reply("Введите формат книги (pdf, epub, mobi):", reply_markup=get_cancel_keyboard())


@router.message(AddBookForm.format)
async def process_format(message: types.Message, state: FSMContext) -> None:
    if message.text == "Отмена":
        await state.clear()
        await message.reply("Добавление книги отменено.",
        reply_markup=get_main_keyboard())
        return
    if message.text.lower() not in ['pdf', 'epub', 'mobi']:
        await message.reply("Формат должен быть pdf, epub или mobi!")
        return
    await state.update_data(format=message.text.lower())
    await state.set_state(AddBookForm.file)
    await message.reply("Отправьте файл книги:",
    reply_markup=get_cancel_keyboard())


@router.message(AddBookForm.file, F.content_type == ContentType.DOCUMENT)
async def process_file(message: types.Message, state: FSMContext) -> None:
    document = message.document
    if document.file_size > 50 * 1024 * 1024:  # 50 MB
        await message.reply("Файл слишком большой! Максимум 50 МБ.")
        await state.clear()
        return
    data = await state.get_data()
    book_service = message.bot.dispatcher.storage.data.get("book_service")  # type: ignore
    try:
        await book_service.add_book(
            title=data['title'],
            author=data['author'],
            format=data['format'],
            file_id=document.file_id,
            file_name=document.file_name
        )
        await message.reply("Книга успешно добавлена!",
        reply_markup=get_main_keyboard())
    except ValueError as e:
        await message.reply(f"Ошибка: {e}",
        reply_markup=get_main_keyboard())
    await state.clear()