from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup, default_state
from utils.keyboards import get_main_keyboard, get_cancel_keyboard
from services.book_service import BookService

router = Router()

class SearchStates(StatesGroup):
    waiting_for_query = State()
#Найти книгу
@router.message(F.text=="Найти книгу", default_state)
async def search_book(message: types.Message, state: FSMContext) -> None:
    """Начало поиска книги"""
    await state.set_state(SearchStates.waiting_for_query)
    await message.reply(
        "Введите название или автора для поиска.",
        reply_markup=get_main_keyboard()
    )
#Обработка поискового запроса
@router.message(SearchStates.waiting_for_query)
async def process_search_query(
        message: types.Message,
        state: FSMContext,
        book_service: BookService
) -> None:
    query = message.text.strip()

    if query == "Отмена":
        await state.clear()
        await message.reply(
            "Поиск отменен.",
            reply_markup=get_main_keyboard()
        )
        return

    books = await book_service.search_books(query)
    if not books:
        await message.reply(
            f"Книги по запросу '{query}' не найдены.",
            reply_markup=get_main_keyboard()
        )
    else:
        response = "\n".join(
            [f"{book.title} by {book.author} ({book.format.upper()})"
             for book in books]
        )
        await message.reply(
            f"Найдены книги:\n{response}",
            reply_markup=get_main_keyboard()
        )
    await state.clear()

